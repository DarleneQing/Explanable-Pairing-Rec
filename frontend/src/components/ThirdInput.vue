<template>
    <WindowLayout>
        <template #header>
            <h1 class="page-title">Choose the Colour</h1>
        </template>

        <template #backButton>
            <BackButton to="/type" :disabled="isSubmitting" />
        </template>

        <template #content>
            <div class="sections-container">
                <div class="section">
                    <h2 class="section-title">(Optional) What colour are you looking for?</h2>
                    <div class="color-grid">
                        <div 
                            v-for="color in availableColors" 
                            :key="color.id"
                            class="color-item"
                            :class="{ active: selectedColor === color.id }"
                            @click="selectedColor = selectedColor === color.id ? '' : color.id"
                        >
                            <button class="color-button">
                                {{ color.name }}
                            </button>
                            <div class="color-swatch" :style="{ backgroundColor: color.hex }">
                                <div class="swatch-overlay"></div>
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
                :disabled="isSubmitting"
            >
                {{ isSubmitting ? 'Saving...' : (selectedColor ? 'Next' : 'Skip') }}
            </button>
        </template>
    </WindowLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useSessionStore } from '@/stores/session';
import { useRouter } from 'vue-router';
import WindowLayout from './WindowLayout.vue';
import BackButton from './BackButton.vue';

const router = useRouter();
const sessionStore = useSessionStore();

const selectedColor = ref('');
const isSubmitting = ref(false);

// Color mapping with hex values for visual representation
const availableColors = [
    { id: 'Black', name: 'Black', hex: '#000000' },
    { id: 'White', name: 'White', hex: '#FFFFFF' },
    { id: 'Blue', name: 'Blue', hex: '#0066CC' },
    { id: 'Grey', name: 'Grey', hex: '#808080' },
    { id: 'Pink', name: 'Pink', hex: '#FFC0CB' },
    { id: 'Lilac Purple', name: 'Lilac Purple', hex: '#B19CD9' },
    { id: 'Brown', name: 'Brown', hex: '#8B4513' },
    { id: 'Red', name: 'Red', hex: '#DC143C' },
    { id: 'Khaki green', name: 'Khaki Green', hex: '#8FBC8F' },
    { id: 'Orange', name: 'Orange', hex: '#FF8C00' },
    { id: 'Yellow', name: 'Yellow', hex: '#FFD700' },
    { id: 'Green', name: 'Green', hex: '#228B22' },
    { id: 'Mole', name: 'Mole', hex: '#392d2b' },
    { id: 'Beige', name: 'Beige', hex: '#F5F5DC' },
    { id: 'Turquoise', name: 'Turquoise', hex: '#30D5C8' },
    { id: 'Metal', name: 'Metal', hex: '#A8A8A8' },
    { id: 'Yellowish Green', name: 'Yellowish Green', hex: '#ADFF2F' },
    { id: 'Bluish Green', name: 'Bluish Green', hex: '#0D98BA' }
];

const canProceed = computed(() => {
    return true; // Always allow proceeding (skip functionality)
});

// Load existing session data on component mount
onMounted(async () => {
    // Ensure we have the latest session data
    await sessionStore.loadStoredSession();
    
    // Try both ways to access the data (handles different Pinia configurations)
    const sessionData = sessionStore.session?.value || (sessionStore.session as any);
    
    if (sessionData?.color) {
        selectedColor.value = sessionData.color;
    }
});

const submitInput = async () => {
    if (!canProceed.value || isSubmitting.value) return;

    isSubmitting.value = true;
    
    try {
        // Update session with selected color
        await sessionStore.updateColor(selectedColor.value);

        console.log('Color updated successfully:', selectedColor.value);

        // Navigate to next page (you can change this route as needed)
        router.push('/appearance');
    } catch (error) {
        console.error('Failed to update color:', error);
        alert('Failed to save your selection. Please try again.');
    } finally {
        isSubmitting.value = false;
    }
};
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

.color-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: var(--space-lg);
    width: 100%;
    max-width: 1000px;
    justify-content: center;
}

.color-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-md);
    cursor: pointer;
    transition: var(--transition-all);
}

.color-item:hover {
    transform: translateY(-2px);
}

.color-item.active .color-button {
    border-color: var(--brand-primary);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
    color: var(--text-inverse);
    box-shadow: 0 4px 12px rgba(var(--brand-primary-rgb), 0.3);
}

.color-item.active .color-swatch {
    border-color: var(--brand-primary);
    box-shadow: 0 4px 12px rgba(var(--brand-primary-rgb), 0.2);
    transform: scale(1.05);
}

.color-item.active .swatch-overlay {
    opacity: 0;
}

.color-button {
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
    text-align: center;
}

.color-button:hover {
    border-color: var(--ui-interactive);
    background: linear-gradient(135deg, rgba(var(--ui-interactive-rgb), 0.08) 0%, rgba(var(--ui-interactive-rgb), 0.04) 100%);
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(var(--ui-text-primary-rgb), 0.1);
}

.color-swatch {
    width: 80px;
    height: 80px;
    border: 3px solid var(--border-light);
    border-radius: var(--border-radius-lg);
    position: relative;
    transition: var(--transition-all);
    box-shadow: 
        inset 0 2px 4px rgba(0, 0, 0, 0.1),
        0 2px 8px rgba(var(--ui-text-primary-rgb), 0.08);
    overflow: hidden;
}

.color-swatch[style*="background-color: #FFFFFF"] {
    border-color: var(--border-light);
    box-shadow: 
        inset 0 2px 4px rgba(0, 0, 0, 0.1),
        0 2px 8px rgba(var(--ui-text-primary-rgb), 0.15),
        0 0 0 1px rgba(0, 0, 0, 0.1);
}

.swatch-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
    opacity: 0.3;
    transition: var(--transition-all);
}

.color-item:hover .color-swatch {
    transform: scale(1.02);
    box-shadow: 
        inset 0 2px 4px rgba(0, 0, 0, 0.1),
        0 4px 12px rgba(var(--ui-text-primary-rgb), 0.12);
}

.color-item:hover .swatch-overlay {
    opacity: 0.1;
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
    .color-grid {
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: var(--space-md);
    }
    
    .color-button {
        min-width: 100px;
        padding: var(--space-sm) var(--space-md);
        font-size: var(--font-size-xs);
    }
    
    .color-swatch {
        width: 70px;
        height: 70px;
    }
}

@media (max-width: 480px) {
    .color-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-sm);
    }
    
    .color-swatch {
        width: 60px;
        height: 60px;
    }
    
    .color-button {
        font-size: var(--font-size-xs);
        padding: var(--space-xs) var(--space-sm);
    }
}
</style>
