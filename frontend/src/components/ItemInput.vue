<template>
    <WindowLayout>
        <template #header>
            <div class="header-container">
                <h1 class="page-title">Choose the Most Similar Item</h1>
                <button class="refresh-button" @click="refreshItems" :disabled="isSubmitting">
                    <img src="/src/assets/refresh.svg" alt="Refresh" class="refresh-icon" />
                </button>
            </div>
        </template>

        <template #backButton>
            <BackButton to="/appearance" :disabled="isSubmitting" />
        </template>

        <template #content>
            <div class="sections-container">
                <div class="section">
                    <h2 class="section-title">Based on your preferences, here are some similar items</h2>
                    <div class="items-grid">
                        <div 
                            v-for="item in candidateItems" 
                            :key="item.id"
                            class="item-card"
                            :class="{ active: selectedItem === item.id }"
                            @click="selectedItem = selectedItem === item.id ? '' : item.id"
                        >
                            <div class="item-image-container">
                                <div class="item-image-placeholder">
                                    <div class="placeholder-content">
                                        <span class="placeholder-text">Item Image</span>
                                    </div>
                                </div>
                            </div>
                            <div class="item-info">
                                <h3 class="item-name">{{ item.name }}</h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template #actions>
            <button 
                class="primary-button" 
                @click="submitSelection"
                :disabled="!canProceed || isSubmitting"
            >
                {{ isSubmitting ? 'Processing...' : 'Get Recommendation' }}
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

const selectedItem = ref('');
const isSubmitting = ref(false);

// Mock candidate items for layout purposes
const candidateItems = [
    { id: 'item-1', name: 'Classic Cotton T-Shirt' },
    { id: 'item-2', name: 'Vintage Denim Jacket' },
    { id: 'item-3', name: 'Striped Button-Up Shirt' },
    { id: 'item-4', name: 'Casual Crew Neck Sweater' },
    { id: 'item-5', name: 'Elegant Silk Blouse' },
    { id: 'item-6', name: 'Modern Fitted Blazer' },
    { id: 'item-7', name: 'Comfortable Hoodie' },
    { id: 'item-8', name: 'Stylish Cardigan' },
    { id: 'item-9', name: 'Stylish Cardigan' }
];

const canProceed = computed(() => {
    return selectedItem.value;
});

// Load existing session data on component mount
onMounted(async () => {
    // Ensure we have the latest session data
    await sessionStore.loadStoredSession();
    console.log('Session loaded for item selection:', sessionStore.session?.value);
});

const submitSelection = async () => {
    if (!canProceed.value || isSubmitting.value) return;

    isSubmitting.value = true;
    
    try {
        console.log('Selected item:', selectedItem.value);
        
        // TODO: Connect to service to save selected item
        // await sessionStore.updateSelectedItem(selectedItem.value);

        // Navigate to next page (results or final screen)
        router.push('/rec-board');
    } catch (error) {
        console.error('Failed to process selection:', error);
        alert('Failed to process your selection. Please try again.');
    } finally {
        isSubmitting.value = false;
    }
};

const refreshItems = () => {
    console.log('Refreshing candidate items...');
    // TODO: Implement refresh logic - could randomize order, fetch new items, etc.
    // For now, we'll just clear the selection and potentially shuffle items
    selectedItem.value = '';
    
    // You can add logic here to:
    // - Fetch new candidate items from API
    // - Shuffle the existing items
    // - Reset any filters or preferences
};
</script>

<style scoped>
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    position: relative;
}

.page-title {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-bold);
    color: var(--brand-primary);
    margin: 0;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}

.refresh-button {
    background: transparent;
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius-md);
    padding: var(--space-sm);
    cursor: pointer;
    transition: var(--transition-all);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    margin-left: auto;
}

.refresh-button:hover:not(:disabled) {
    border-color: var(--ui-interactive);
    background: rgba(var(--ui-interactive-rgb), 0.08);
    transform: scale(1.05);
}

.refresh-button:active:not(:disabled) {
    transform: scale(0.98);
}

.refresh-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.refresh-icon {
    width: 20px;
    height: 20px;
    transition: var(--transition-all);
}

.refresh-button:hover:not(:disabled) .refresh-icon {
    transform: rotate(180deg);
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

.items-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: var(--space-xl);
    width: 100%;
    max-width: 1000px;
    justify-content: center;
}

.item-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: var(--transition-all);
    padding: var(--space-md);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius-lg);
    background: linear-gradient(135deg, var(--ui-bg) 0%, var(--ui-bg-secondary) 100%);
    box-shadow: 0 2px 8px rgba(var(--ui-text-primary-rgb), 0.08);
}

.item-card:hover {
    transform: translateY(-4px);
    border-color: var(--ui-interactive);
    box-shadow: 0 8px 20px rgba(var(--ui-text-primary-rgb), 0.15);
}

.item-card.active {
    border-color: var(--brand-primary);
    background: linear-gradient(135deg, rgba(var(--brand-primary-rgb), 0.05) 0%, rgba(var(--brand-secondary-rgb), 0.05) 100%);
    box-shadow: 0 8px 20px rgba(var(--brand-primary-rgb), 0.25);
    transform: translateY(-4px);
}

.item-image-container {
    width: 100%;
    margin-bottom: var(--space-md);
}

.item-image-placeholder {
    width: 100%;
    height: 180px;
    border: 2px dashed var(--border-light);
    border-radius: var(--border-radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--ui-bg-secondary);
    transition: var(--transition-all);
    overflow: hidden;
}

.item-card.active .item-image-placeholder {
    border-color: var(--brand-primary);
    background: rgba(var(--brand-primary-rgb), 0.05);
}

.placeholder-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: var(--space-sm);
}

.placeholder-text {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    font-weight: var(--font-weight-medium);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.item-card.active .placeholder-text {
    color: var(--brand-primary);
    font-weight: var(--font-weight-bold);
}

.item-info {
    width: 100%;
    text-align: center;
}

.item-name {
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    margin: 0;
    line-height: 1.4;
    padding: 0 var(--space-xs);
}

.item-card.active .item-name {
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

/* Responsive Design */
@media (max-width: 1024px) {
    .items-grid {
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
        gap: var(--space-lg);
        max-width: 800px;
    }
    
    .item-image-placeholder {
        height: 160px;
    }
}

@media (max-width: 768px) {
    .items-grid {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(4, 1fr);
        gap: var(--space-md);
        max-width: 600px;
    }
    
    .item-image-placeholder {
        height: 140px;
    }
    
    .item-name {
        font-size: var(--font-size-xs);
    }
    
    .item-card {
        padding: var(--space-sm);
    }
}

@media (max-width: 480px) {
    .items-grid {
        grid-template-columns: 1fr;
        grid-template-rows: repeat(8, 1fr);
        gap: var(--space-sm);
        max-width: 400px;
    }
    
    .item-image-placeholder {
        height: 120px;
    }
    
    .section-title {
        font-size: var(--font-size-md);
    }
}
</style>


