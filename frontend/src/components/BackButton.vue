<template>
    <button 
        class="back-button" 
        @click="goBack"
        :disabled="disabled"
    >
        ← Back
    </button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

interface Props {
    to: string
    disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
    disabled: false
})

const router = useRouter()

const goBack = () => {
    router.push(props.to)
}
</script>

<style scoped>
.back-button {
    background: var(--window-color1);
    color: var(--text-primary);
    padding: var(--space-sm) var(--space-md);
    border: 2px solid var(--window-color3);
    border-radius: var(--border-radius-md);
    cursor: pointer;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    transition: var(--transition-all);
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    min-width: 80px;
    justify-content: center;
}

.back-button:hover:not(:disabled) {
    background: var(--window-color3);
    transform: translateY(-1px);
    color: var(--text-inverse);
}

.back-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style> 