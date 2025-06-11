<template>
    <div class="window-wrapper">
        <div class="window-container">
            <div class="window-header" v-if="$slots.header">
                <div class="header-content">
                    <slot name="header"></slot>
                </div>
                <div class="header-back-button" v-if="$slots.backButton">
                    <slot name="backButton"></slot>
                </div>
            </div>
            
            <div class="window-content">
                <slot name="content"></slot>
            </div>
            
            <div class="window-actions" v-if="$slots.actions">
                <slot name="actions"></slot>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    maxWidth: {
        type: String,
        default: '800px'
    },
    height: {
        type: String,
        default: '90%'
    },
    maxHeight: {
        type: String,
        default: '600px'
    },
    minHeight: {
        type: String,
        default: '400px'
    }
})
</script>

<style scoped>
.window-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1; /* Take remaining space after header */
    padding: var(--space-xl) var(--space-lg);
    overflow: hidden; /* Prevent page scroll */
}

.window-container {
    display: flex;
    flex-direction: column;
    max-width: v-bind(maxWidth);
    width: 100%;
    height: v-bind(height);
    max-height: v-bind(maxHeight);
    min-height: v-bind(minHeight);
    background: linear-gradient(135deg, var(--ui-bg-elevated) 0%, var(--window-color2) 100%);
    border-radius: var(--border-radius-2xl);
    box-shadow: 
        0 25px 60px rgba(var(--ui-text-primary-rgb), 0.25),
        0 12px 24px rgba(var(--ui-text-primary-rgb), 0.15),
        0 6px 12px rgba(var(--ui-text-primary-rgb), 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    border: 2px solid rgba(var(--ui-interactive-rgb), 0.3);
    position: relative;
    overflow: hidden;
    transform: translateY(-4px);
}

.window-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, 
        var(--brand-primary), 
        var(--ui-interactive), 
        var(--ui-interactive-brown),
        var(--brand-secondary)
    );
    border-radius: var(--border-radius-2xl) var(--border-radius-2xl) 0 0;
    z-index: 1;
}

.window-container::after {
    content: '';
    position: absolute;
    top: 6px;
    left: 0;
    right: 0;
    height: 1px;
    background: rgba(var(--ui-text-primary-rgb), 0.1);
    z-index: 1;
}

.window-header {
    flex-shrink: 0;
    position: relative;
    padding: var(--space-3xl) var(--space-3xl) var(--space-lg) var(--space-3xl);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(var(--window-color1-rgb), 0.5) 100%);
    z-index: 2;
    border-bottom: 1px solid rgba(var(--ui-border-medium-rgb), 0.3);
}

.header-content {
    text-align: center;
}

.header-back-button {
    position: absolute;
    top: var(--space-lg);
    left: var(--space-lg);
    z-index: 3;
}

.window-content {
    flex: 1;
    overflow-y: auto;
    padding: 0 var(--space-3xl);
    margin-bottom: var(--space-lg);
}

/* Custom scrollbar styling */
.window-content::-webkit-scrollbar {
    width: 6px;
}

.window-content::-webkit-scrollbar-track {
    background: var(--window-color1);
    border-radius: 3px;
}

.window-content::-webkit-scrollbar-thumb {
    background: var(--window-color3);
    border-radius: 3px;
    transition: var(--transition-colors);
}

.window-content::-webkit-scrollbar-thumb:hover {
    background: var(--font-color1);
}

.window-actions {
    flex-shrink: 0;
    display: flex;
    gap: var(--space-md);
    flex-wrap: wrap;
    justify-content: center;
    padding: var(--space-lg) var(--space-3xl) var(--space-2xl) var(--space-3xl);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(var(--window-color1-rgb), 0.4) 100%);
    border-top: 1px solid rgba(var(--ui-border-medium-rgb), 0.3);
}

/* Responsive design */
@media (max-width: 768px) {
    .window-wrapper {
        padding: var(--space-lg) var(--space-md);
        overflow: hidden;
    }
    
    .window-container {
        height: 90%; /* Use more space on smaller screens */
        max-height: 550px;
        min-height: 350px;
        max-width: none;
    }
    
    .window-header {
        padding: var(--space-xl) var(--space-2xl) var(--space-md) var(--space-2xl);
    }
    
    .window-content {
        padding: 0 var(--space-2xl);
    }
    
    .window-actions {
        padding: var(--space-md) var(--space-2xl) var(--space-lg) var(--space-2xl);
        flex-direction: column;
        align-items: stretch;
    }
}

@media (max-width: 480px) {
    .window-wrapper {
        padding: var(--space-md);
        overflow: hidden;
    }
    
    .window-container {
        height: 95%; /* Almost full height on mobile */
        max-height: 450px;
        min-height: 300px;
    }
    
    .window-header {
        padding: var(--space-lg) var(--space-lg) var(--space-sm) var(--space-lg);
    }
    
    .window-content {
        padding: 0 var(--space-lg);
    }
    
    .window-actions {
        padding: var(--space-sm) var(--space-lg) var(--space-md) var(--space-lg);
    }
}
</style> 