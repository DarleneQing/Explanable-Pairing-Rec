<template>
    <WindowLayout>
        <template #header>
            <h1 class="page-title">Welcome to PairSynergy, your journey starts here</h1>
        </template>
        
        <template #content>
            <div class="sections-container">
                <!-- Section 1: Name Input -->
                <div class="section">
                    <h2 class="section-title">What's your name?</h2>
                    <div class="input-container">
                        <input 
                            type="text" 
                            v-model="userName" 
                            placeholder="Enter your name here" 
                            class="input-field"
                        />
                    </div>
                </div>

                <!-- Section 2: Exploration Choice -->
                <div class="section">
                    <h2 class="section-title">What do you want to explore?</h2>
                    <div class="button-group">
                        <button 
                            class="choice-button"
                            :class="{ active: selectedExploration === 'ladieswear' }"
                            @click="selectedExploration = selectedExploration === 'ladieswear' ? '' : 'ladieswear'"
                        >
                            Ladieswear
                        </button>
                        <button 
                            class="choice-button"
                            :class="{ active: selectedExploration === 'menswear' }"
                            @click="selectedExploration = selectedExploration === 'menswear' ? '' : 'menswear'"
                        >
                            Menswear
                        </button>
                    </div>
                </div>

                <!-- Section 3: Starting Category -->
                <div class="section">
                    <h2 class="section-title">I want to start with...</h2>
                    <div class="category-grid">
                        <div 
                            v-for="category in categories" 
                            :key="category.id"
                            class="category-item"
                            :class="{ active: selectedCategory === category.id }"
                            @click="selectedCategory = selectedCategory === category.id ? '' : category.id"
                        >
                            <button class="category-button">
                                {{ category.name }}
                            </button>
                            <div class="image-placeholder">
                                <div class="placeholder-content">
                                    <img :src="category.image" :alt="category.name">
                                </div>
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
import { useSessionStore } from '../stores/session'

const router = useRouter()
const sessionStore = useSessionStore()

const userName = ref('')
const selectedExploration = ref('')
const selectedCategory = ref('')
const isSubmitting = ref(false)

const categories = [
    { id: 'top', name: 'Top', image: '/src/assets/outlines/T-shirt.png' , as: 'Garment Upper body'},
    { id: 'bottom', name: 'Bottom', image: '/src/assets/outlines/bottom.png' , as: 'Garment Lower body'},
    { id: 'full body', name: 'Full Body', image: '/src/assets/outlines/full-body.png' , as: 'Garment Full body'},
    { id: 'shoes', name: 'Shoes', image: '/src/assets/outlines/Shoes.png' , as: 'Shoes'},
    { id: 'accessories', name: 'Accessories', image: '/src/assets/outlines/accessory.png' , as: 'Accessories'}
]

const canProceed = computed(() => {
    return userName.value.trim() && selectedExploration.value && selectedCategory.value
})

// Load existing session data on component mount
onMounted(async () => {
    // Ensure we have the latest session data
    await sessionStore.loadStoredSession();
    
    // Try both ways to access the data (handles different Pinia configurations)
    const sessionData = sessionStore.session?.value || (sessionStore.session as any);
    
    if (sessionData) {
        userName.value = sessionData.name || ''
        selectedExploration.value = sessionData.section || ''
        
        // Map garment_group back to category id
        const categoryMap: Record<string, string> = {
            'Garment Upper body': 'top',
            'Garment Lower body': 'bottom', 
            'Garment Full body': 'full body',
            'Shoes': 'shoes',
            'Accessories': 'accessories'
        }
        
        if (sessionData.garment_group) {
            selectedCategory.value = categoryMap[sessionData.garment_group] || ''
        }
    }
})

const submitInput = async () => {
    if (!canProceed.value || isSubmitting.value) return

    isSubmitting.value = true
    
    try {
        // Find the selected category to get its 'as' property
        const selectedCategoryObj = categories.find(cat => cat.id === selectedCategory.value)
        const garmentGroup = selectedCategoryObj?.as || selectedCategory.value
        
        // Update session with user inputs
        await sessionStore.updateSessionData({
            name: userName.value.trim(),
            section: selectedExploration.value,
            garment_group: garmentGroup
        })

        console.log('Session updated successfully:', {
            name: userName.value,
            exploration: selectedExploration.value,
            category: selectedCategory.value,
            garmentGroup: garmentGroup
        })

        // Navigate to next page (you can change this route as needed)
        router.push('/type')
    } catch (error) {
        console.error('Failed to update session:', error)
        // You might want to show an error message to the user
        alert('Failed to save your inputs. Please try again.')
    } finally {
        isSubmitting.value = false
    }
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

.input-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.input-field {
    width: 100%;
    max-width: 400px;
    padding: var(--space-md);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius-lg);
    font-size: var(--font-size-sm);
    color: var(--text-primary);
    background: var(--ui-bg);
    transition: var(--transition-all);
    text-align: center;
}

.input-field:focus {
    outline: none;
    border-color: var(--ui-interactive);
    box-shadow: 0 0 0 3px rgba(var(--ui-interactive-rgb), 0.1);
}

.input-field::placeholder {
    color: var(--text-secondary);
}

.button-group {
    display: flex;
    gap: var(--space-lg);
    flex-wrap: wrap;
    justify-content: center;
}

.choice-button {
    padding: var(--space-md) var(--space-xl);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius-lg);
    background: linear-gradient(135deg, var(--ui-bg) 0%, var(--ui-bg-secondary) 100%);
    color: var(--text-primary);
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    cursor: pointer;
    transition: var(--transition-all);
    min-width: 140px;
    box-shadow: 0 2px 8px rgba(var(--ui-text-primary-rgb), 0.08);
}

.choice-button:hover {
    border-color: var(--ui-interactive);
    background: linear-gradient(135deg, rgba(var(--ui-interactive-rgb), 0.1) 0%, rgba(var(--ui-interactive-rgb), 0.05) 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(var(--ui-text-primary-rgb), 0.12);
}

.choice-button.active {
    border-color: var(--brand-primary);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
    color: var(--text-inverse);
    box-shadow: 0 4px 12px rgba(var(--brand-primary-rgb), 0.3);
}

.category-grid {
    display: flex;
    gap: var(--space-lg);
    width: 100%;
    max-width: 800px;
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

.placeholder-content img {
    max-width: 80%;
    max-height: 80%;
    object-fit: contain;
    filter: grayscale(20%) opacity(0.8);
    transition: var(--transition-all);
}

.category-item.active .placeholder-content img {
    filter: none;
    opacity: 1;
}

.placeholder-text {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    font-weight: var(--font-weight-medium);
    text-transform: uppercase;
    letter-spacing: 0.5px;
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

@media (max-width: 768px) {
    .category-grid {
        gap: var(--space-md);
        flex-wrap: wrap;
    }
    
    .category-item {
        flex: 1;
        min-width: 120px;
    }
    
    .image-placeholder {
        width: 100px;
        height: 100px;
    }
    
    .button-group {
        gap: var(--space-md);
    }
    
    .choice-button {
        min-width: 120px;
        padding: var(--space-sm) var(--space-lg);
    }
}
</style> 