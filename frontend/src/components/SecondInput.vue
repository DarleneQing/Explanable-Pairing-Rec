<template>
    <WindowLayout>
        <template #header>
            <h1 class="page-title">Choose the specific product type</h1>
        </template>
        
        <template #backButton>
            <BackButton to="/" :disabled="isSubmitting" />
        </template>
        
        <template #content>
            <div class="sections-container">
                <!-- Section 1: Type Selection -->
                <div class="section">
                    <h2 class="section-title">What type of garment are you looking for?</h2>
                    <div v-if="availableTypes.length === 0" class="no-types-message">
                        <p>No product types available. Please go back and select a category first.</p>
                        <button @click="refreshSession" class="refresh-button">Refresh Session Data</button>
                    </div>
                    <div v-else class="category-grid">
                        <div 
                            v-for="type in availableTypes" 
                            :key="type.id"
                            class="category-item"
                            :class="{ active: selectedType === type.id }"
                            @click="selectedType = selectedType === type.id ? '' : type.id"
                        >
                            <button class="category-button">
                                {{ type.name }}
                            </button>
                            <div class="image-placeholder">
                                <img 
                                    :src="type.imagePath" 
                                    :alt="type.name"
                                    class="type-image"
                                    @error="handleImageError"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template #actions>
            <button 
                class="primary-button" 
                @click="submitInput"
                :disabled="!canProceed || isSubmitting"
            >
                {{ isSubmitting ? 'Saving...' : 'Next' }}
            </button>
        </template>
    </WindowLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WindowLayout from './WindowLayout.vue'
import BackButton from './BackButton.vue'
import { useSessionStore } from '../stores/session'

// Define the type interface
interface ProductType {
    id: string
    name: string
    imagePath: string
}

const router = useRouter()
const sessionStore = useSessionStore()

const selectedType = ref('')
const isSubmitting = ref(false)
const sessionLoaded = ref(false)

// Product type mappings based on category.txt
const typeMappingLadieswear: Record<string, string[]> = {
    'Garment Upper body': ['Vest Top', 'T-shirt', 'Top', 'Shirt', 'Sweater', 'Cardigan', 'Hoodie', 'Blazer', 'Jacket', 'Blouse', 'Coat', 'Bodysuit'],
    'Garment Lower body': ['Trousers', 'Skirt', 'Shorts'],
    'Garment Full body': ['Dress', 'Dungarees', 'Jumpsuit'],
    'Shoes': ['Sandals', 'Heels','Flat shoes', 'Boots', 'Sneakers'],
    'Accessories': ['Glasses', 'Hat', 'Jewelry', 'Scarf', 'Belt', 'Gloves', 'Bag']
}

const typeMappingMenswear: Record<string, string[]> = {
    'Garment Upper body': ['Vest Top', 'Top', 'Sweater', 'T-shirt', 'Shirt', 'Cardigan', 'Hoodie', 'Blazer', 'Jacket', 'Coat'],
    'Garment Lower body': ['Trousers', 'Shorts'],
    'Garment Full body': ['Dungarees'],
    'Shoes': ['Boots', 'Sneakers', 'Sandals', 'Flat shoes'],
    'Accessories': ['Glasses', 'Hat', 'Jewelry', 'Scarf', 'Gloves', 'Bag']
}

const availableTypes = computed(() => {
    // Force reactivity by accessing the session store reactively
    // Also depend on sessionLoaded to trigger re-computation
    const session = sessionStore.session
    const isLoaded = sessionLoaded.value
    // @ts-ignore: Pinia auto-unwraps refs, this works at runtime
    const garmentGroup = session?.garment_group
    // @ts-ignore: Pinia auto-unwraps refs, this works at runtime
    const section = session?.section
    
    console.log('Session loaded:', isLoaded)
    console.log('Session garment_group:', garmentGroup)
    console.log('Session section:', section)
    console.log('Full session:', session)
    
    if (!isLoaded || !garmentGroup || !section) {
        console.log('Session not loaded or missing garment group/section')
        return []
    }
    
    // Choose the appropriate mapping based on section
    const typeMapping = section === 'menswear' ? typeMappingMenswear : typeMappingLadieswear
    console.log('Using mapping for:', section)
    console.log('Available mapping keys:', Object.keys(typeMapping))
    
    if (!typeMapping[garmentGroup]) {
        console.log('No matching mapping found for garment group:', garmentGroup)
        return []
    }
    
    const types = typeMapping[garmentGroup].map(type => ({
        id: type,
        name: type,
        imagePath: getImagePath(type, garmentGroup, section)
    }))
    console.log('Available types:', types)
    return types
})

// Function to get the correct image path for each product type
const getImagePath = (productType: string, garmentGroup: string, section: string) => {
    try {
        // Handle special cases for shoes with gender-specific images
        if (garmentGroup === 'Shoes') {
            const genderSuffix = section === 'menswear' ? 'Men' : 'Women'
            
            // Map product types to their image names
            const shoeImageMap: Record<string, string> = {
                'Sandals': `Sandals-${genderSuffix}.png`,
                'Flat shoes': `Flat shoes-${genderSuffix}.png`,
                'Boots': `Boots-${genderSuffix}.png`,
                'Sneakers': 'Sneakers.png',
                'Heels': 'Heels.png' // Only for women
            }
            
            const imageName = shoeImageMap[productType]
            if (imageName) {
                return `/src/assets/outlines/Shoes/${imageName}`
            }
        }
        
        // Handle special naming cases
        const nameMap: Record<string, string> = {
            'Hoodie': 'Hoodies.png' // The file is named Hoodies.png, not Hoodie.png
        }
        
        const imageName = nameMap[productType] || `${productType}.png`
        return `/src/assets/outlines/${garmentGroup}/${imageName}`
    } catch (error) {
        console.warn(`Image not found for ${productType}:`, error)
        return '/src/assets/outlines/T-shirt.png' // Fallback image
    }
}

const canProceed = computed(() => {
    return selectedType.value
})

// Load existing session data on component mount
onMounted(async () => {
    // Ensure we have the latest session data
    await sessionStore.loadStoredSession()
    
    // Try both ways to access the data (handles different Pinia configurations)
    const sessionData = sessionStore.session?.value || (sessionStore.session as any);
    
    if (sessionData?.product_type) {
        selectedType.value = sessionData.product_type
    }
    sessionLoaded.value = true
})

const refreshSession = async () => {
    console.log('Manually refreshing session...')
    await sessionStore.loadStoredSession()
    console.log('Session refreshed:', sessionStore.session?.value)
    sessionLoaded.value = true
}

const submitInput = async () => {
    if (!canProceed.value || isSubmitting.value) return
    isSubmitting.value = true

    try {
        await sessionStore.updateProductType(selectedType.value)

        console.log('Product type updated successfully:', selectedType.value)

        // Navigate to next page
        router.push('/color')
    } catch (error) {
        console.error('Failed to update product type:', error)
        alert('Failed to save your selection. Please try again.')
    } finally {
        isSubmitting.value = false
    }
}

// Function to handle image loading errors
const handleImageError = (event: Event) => {
    const img = event.target as HTMLImageElement
    console.warn(`Failed to load image: ${img.src}`)
    // Set fallback image
    img.src = '/src/assets/outlines/T-shirt.png'
}
</script>

<style scoped>
.page-title {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-bold);
    color: var(--brand-primary);
    margin: 0;
}

.sections-container {
    display: flex;
    flex-direction: column;
    gap: var(--space-2xl);
    padding: var(--space-xl) 0;
}

.section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-lg);
}

.section-title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    margin: 0;
    text-align: center;
}

.category-grid {
    display: flex;
    gap: var(--space-lg);
    width: 100%;
    max-width: 1000px;
    justify-content: center;
    flex-wrap: wrap;
}

.category-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-md);
    cursor: pointer;
    transition: var(--transition-all);
}

.category-item:hover {
    transform: translateY(-2px);
}

.category-item.active .category-button {
    border-color: var(--brand-primary);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
    color: var(--text-inverse);
    box-shadow: 0 4px 12px rgba(var(--brand-primary-rgb), 0.3);
}

.category-item.active .image-placeholder {
    border-color: var(--brand-primary);
    box-shadow: 0 4px 12px rgba(var(--brand-primary-rgb), 0.2);
}

.category-button {
    padding: var(--space-sm) var(--space-lg);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius-lg);
    background: linear-gradient(135deg, var(--ui-bg) 0%, var(--ui-bg-secondary) 100%);
    color: var(--text-primary);
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    cursor: pointer;
    transition: var(--transition-all);
    width: 100%;
    box-shadow: 0 2px 6px rgba(var(--ui-text-primary-rgb), 0.06);
    min-width: 120px;
}

.category-button:hover {
    border-color: var(--ui-interactive);
    background: linear-gradient(135deg, rgba(var(--ui-interactive-rgb), 0.08) 0%, rgba(var(--ui-interactive-rgb), 0.04) 100%);
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(var(--ui-text-primary-rgb), 0.1);
}

.image-placeholder {
    width: 120px;
    height: 120px;
    border: 2px dashed var(--border-light);
    border-radius: var(--border-radius-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--ui-bg-secondary);
    transition: var(--transition-all);
    overflow: hidden;
}

.type-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: center;
    filter: opacity(0.8);
    transition: var(--transition-all);
}

.category-item.active .type-image {
    filter: opacity(1);
}

.category-item:hover .type-image {
    filter: opacity(0.9);
    transform: scale(1.05);
}

.placeholder-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: var(--space-sm);
    width: 100%;
    height: auto;
}

.placeholder-text {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    font-weight: var(--font-weight-medium);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.category-item.active .placeholder-text {
    color: var(--brand-primary);
    font-weight: var(--font-weight-bold);
}

.primary-button {
    background: linear-gradient(135deg, var(--ui-interactive) 0%, var(--ui-interactive-brown) 100%);
    color: var(--text-inverse);
    padding: var(--space-md) var(--space-xl);
    border: none;
    border-radius: var(--border-radius-lg);
    cursor: pointer;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    box-shadow: 
        0 4px 12px rgba(var(--ui-interactive-rgb), 0.3),
        0 2px 4px rgba(var(--ui-text-primary-rgb), 0.1);
    transition: var(--transition-all);
    border: 1px solid rgba(var(--ui-interactive-rgb), 0.5);
}

.primary-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 
        0 6px 20px rgba(var(--ui-interactive-rgb), 0.4),
        0 4px 8px rgba(var(--ui-text-primary-rgb), 0.15);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
}

.primary-button:active:not(:disabled) {
    transform: translateY(0);
}

.primary-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.no-types-message {
    text-align: center;
    padding: var(--space-xl);
    background-color: var(--ui-bg-secondary);
    border-radius: var(--border-radius-lg);
    margin-bottom: var(--space-xl);
}

.no-types-message p {
    color: var(--text-primary);
    margin: var(--space-sm) 0;
}

.no-types-message small {
    color: var(--text-secondary);
}

.refresh-button {
    background: linear-gradient(135deg, var(--ui-interactive) 0%, var(--ui-interactive-brown) 100%);
    color: var(--text-inverse);
    padding: var(--space-md) var(--space-xl);
    border: none;
    border-radius: var(--border-radius-lg);
    cursor: pointer;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    box-shadow: 
        0 4px 12px rgba(var(--ui-interactive-rgb), 0.3),
        0 2px 4px rgba(var(--ui-text-primary-rgb), 0.1);
    transition: var(--transition-all);
    border: 1px solid rgba(var(--ui-interactive-rgb), 0.5);
    margin-top: var(--space-md);
}

.refresh-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 
        0 6px 20px rgba(var(--ui-interactive-rgb), 0.4),
        0 4px 8px rgba(var(--ui-text-primary-rgb), 0.15);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
}

.refresh-button:active:not(:disabled) {
    transform: translateY(0);
}

.refresh-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

@media (max-width: 768px) {
    .category-grid {
        gap: var(--space-md);
        flex-wrap: wrap;
    }
    
    .category-item {
        flex: 1;
        min-width: 100px;
    }
    
    .image-placeholder {
        width: 100px;
        height: 100px;
    }
    
    .category-button {
        min-width: 100px;
        padding: var(--space-sm) var(--space-md);
        font-size: var(--font-size-xs);
    }
}
</style>