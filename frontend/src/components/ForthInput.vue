<template>
    <WindowLayout>
        <template #header>
            <h1 class="page-title">Choose the Graphical Appearance</h1>
        </template>

        <template #backButton>
            <BackButton to="/color" :disabled="isSubmitting" />
        </template>

        <template #content>
            <div class="sections-container">
                <div class="section">
                    <h2 class="section-title">(Optional) What graphical appearance are you looking for?</h2>
                    <div class="appearance-grid">
                        <div 
                            v-for="appearance in availableAppearances" 
                            :key="appearance.id"
                            class="appearance-item"
                            :class="{ active: selectedAppearance === appearance.id }"
                            @click="selectedAppearance = selectedAppearance === appearance.id ? '' : appearance.id"
                        >
                            <button class="appearance-button">
                                {{ appearance.name }}
                            </button>
                            <div class="appearance-preview">
                                <img 
                                    v-if="getImagePath(appearance.id)" 
                                    :src="getImagePath(appearance.id)" 
                                    :alt="appearance.name"
                                    class="appearance-image"
                                    @error="handleImageError"
                                />
                                <div v-else class="fallback-pattern">
                                    <span class="pattern-text">{{ appearance.short }}</span>
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
                :disabled="isSubmitting"
            >
                {{ isSubmitting ? 'Saving...' : (selectedAppearance ? 'Next' : 'Skip') }}
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

const selectedAppearance = ref('');
const isSubmitting = ref(false);

// Graphical appearance options with display names and short descriptors
const availableAppearances = [
    { id: 'Solid', name: 'Solid', short: 'Plain' },
    { id: 'Stripe', name: 'Stripe', short: 'Lines' },
    { id: 'Melange', name: 'Melange', short: 'Mixed' },
    { id: 'All over pattern', name: 'All Over Pattern', short: 'Full' },
    { id: 'Check', name: 'Check', short: 'Grid' },
    { id: 'Glittering/Metallic', name: 'Glittering/Metallic', short: 'Shine' },
    { id: 'Neps', name: 'Neps', short: 'Fleck' },
    { id: 'Placement print', name: 'Placement Print', short: 'Local' },
    { id: 'Denim', name: 'Denim', short: 'Jean' },
    { id: 'Treatment', name: 'Treatment', short: 'Finish' },
    { id: 'Transparent', name: 'Transparent', short: 'Clear' },
    { id: 'Embroidery', name: 'Embroidery', short: 'Stitch' },
    { id: 'Chambray', name: 'Chambray', short: 'Weave' },
    { id: 'Dot', name: 'Dot', short: 'Spots' },
    { id: 'Contrast', name: 'Contrast', short: 'Pop' },
    { id: 'Jacquard', name: 'Jacquard', short: 'Woven' },
    { id: 'Metallic', name: 'Metallic', short: 'Metal' },
    { id: 'Colour blocking', name: 'Colour Blocking', short: 'Block' },
    { id: 'Argyle', name: 'Argyle', short: 'Diamond' },
    { id: 'Front print', name: 'Front Print', short: 'Front' },
    { id: 'Mixed solid/pattern', name: 'Mixed Solid/Pattern', short: 'Combo' },
    { id: 'Lace', name: 'Lace', short: 'Open' },
    { id: 'Slub', name: 'Slub', short: 'Thick' },
    { id: 'Mesh', name: 'Mesh', short: 'Net' },
    { id: 'Sequin', name: 'Sequin', short: 'Disc' },
    { id: 'Hologram', name: 'Hologram', short: 'Holo' }
];

// Function to get the correct image path for each appearance type
const getImagePath = (appearanceId: string) => {
    // Map appearance IDs to their actual filenames
    const imageMap: Record<string, string> = {
        'Solid': '', // No image for solid, will use fallback
        'Stripe': 'Stripe.png',
        'Melange': 'Melange.png',
        'All over pattern': 'All over pattern.png',
        'Check': 'Check.png',
        'Glittering/Metallic': 'Glittering.png',
        'Neps': 'Neps.png',
        'Placement print': 'Placement print.png',
        'Denim': 'Denim.png',
        'Treatment': 'Treatment.png',
        'Transparent': 'Transparent.png',
        'Embroidery': 'Embroidery.png',
        'Chambray': 'Chambray.png',
        'Dot': 'Dot.png',
        'Contrast': 'Contrast.png',
        'Jacquard': 'Jacquard.png',
        'Metallic': 'Metallic.png',
        'Colour blocking': 'Colour blocking.png',
        'Argyle': 'Argyle.png',
        'Front print': 'Front print.png',
        'Mixed solid/pattern': 'Mixed solid pattern.png',
        'Lace': 'Lace.png',
        'Slub': 'Slub.png',
        'Mesh': 'Mesh.png',
        'Sequin': 'Sequin.png',
        'Hologram': 'Hologram.png'
    };
    
    const filename = imageMap[appearanceId];
    if (filename) {
        return `/src/assets/Appearance/${filename}`;
    }
    return null; // No image available
};

// Function to handle image loading errors
const handleImageError = (event: Event) => {
    const img = event.target as HTMLImageElement;
    console.warn(`Failed to load appearance image: ${img.src}`);
    // Hide the image and show the pattern text instead
    img.style.display = 'none';
};

const canProceed = computed(() => {
    return true; // Always allow proceeding (skip functionality)
});

// Load existing session data on component mount
onMounted(async () => {
    // Ensure we have the latest session data
    await sessionStore.loadStoredSession();
    
    // Try both ways to access the data (handles different Pinia configurations)
    const sessionData = sessionStore.session?.value || (sessionStore.session as any);
    
    if (sessionData?.graphic_appearance) {
        selectedAppearance.value = sessionData.graphic_appearance;
    }
});

const submitInput = async () => {
    if (!canProceed.value || isSubmitting.value) return;

    isSubmitting.value = true;
    
    try {
        // Debug: Check if the function exists
        console.log('sessionStore:', sessionStore);
        console.log('Available methods:', Object.keys(sessionStore));
        console.log('updateGraphicAppearance function:', typeof sessionStore.updateGraphicAppearance);
        
        // Alternative approach: Try to get a fresh store instance if the method is missing
        if (typeof sessionStore.updateGraphicAppearance !== 'function') {
            console.warn('updateGraphicAppearance not found, trying fresh store instance...');
            const freshStore = useSessionStore();
            if (typeof freshStore.updateGraphicAppearance === 'function') {
                await freshStore.updateGraphicAppearance(selectedAppearance.value);
            } else {
                throw new Error('updateGraphicAppearance method is not available even on fresh store instance');
            }
        } else {
            // Update session with selected graphic appearance
            await sessionStore.updateGraphicAppearance(selectedAppearance.value);
        }

        console.log('Graphic appearance updated successfully:', selectedAppearance.value);

        // Navigate to next page (you can change this route as needed)
        router.push('/item');
    } catch (error) {
        console.error('Failed to update graphic appearance:', error);
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

.appearance-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: var(--space-lg);
    width: 100%;
    max-width: 1200px;
    justify-content: center;
}

.appearance-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-md);
    cursor: pointer;
    transition: var(--transition-all);
}

.appearance-item:hover {
    transform: translateY(-2px);
}

.appearance-item.active .appearance-button {
    border-color: var(--brand-primary);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
    color: var(--text-inverse);
    box-shadow: 0 4px 12px rgba(var(--brand-primary-rgb), 0.3);
}

.appearance-item.active .appearance-preview {
    border-color: var(--brand-primary);
    box-shadow: 0 4px 12px rgba(var(--brand-primary-rgb), 0.2);
}

.appearance-button {
    padding: var(--space-sm) var(--space-md);
    border: 2px solid var(--border-light);
    border-radius: var(--border-radius-lg);
    background: linear-gradient(135deg, var(--ui-bg) 0%, var(--ui-bg-secondary) 100%);
    color: var(--text-primary);
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-semibold);
    cursor: pointer;
    transition: var(--transition-all);
    width: 100%;
    box-shadow: 0 2px 6px rgba(var(--ui-text-primary-rgb), 0.06);
    min-width: 140px;
    text-align: center;
}

.appearance-button:hover {
    border-color: var(--ui-interactive);
    background: linear-gradient(135deg, rgba(var(--ui-interactive-rgb), 0.08) 0%, rgba(var(--ui-interactive-rgb), 0.04) 100%);
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(var(--ui-text-primary-rgb), 0.1);
}

.appearance-preview {
    width: 100px;
    height: 80px;
    border: 2px dashed var(--border-light);
    border-radius: var(--border-radius-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--ui-bg-secondary);
    transition: var(--transition-all);
    overflow: hidden;
    position: relative;
}

.appearance-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    filter: opacity(0.8);
    transition: var(--transition-all);
}

.appearance-item.active .appearance-image {
    filter: opacity(1);
}

.appearance-item:hover .appearance-image {
    filter: opacity(0.9);
    transform: scale(1.05);
}

.fallback-pattern {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--ui-bg) 0%, var(--ui-bg-secondary) 100%);
}

.pattern-text {
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-bold);
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    z-index: 2;
}

.appearance-item.active .pattern-text {
    color: var(--brand-primary);
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
    .appearance-grid {
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: var(--space-md);
    }
    
    .appearance-button {
        min-width: 120px;
        padding: var(--space-xs) var(--space-sm);
        font-size: var(--font-size-xs);
    }
    
    .appearance-preview {
        width: 90px;
        height: 70px;
    }
}

@media (max-width: 480px) {
    .appearance-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-sm);
    }
    
    .appearance-preview {
        width: 80px;
        height: 60px;
    }
    
    .appearance-button {
        font-size: var(--font-size-xs);
        padding: var(--space-xs) var(--space-sm);
    }
}
</style>


