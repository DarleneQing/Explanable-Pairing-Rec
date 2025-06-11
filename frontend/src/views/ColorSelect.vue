<script setup lang="ts">
import Header from '../components/Header.vue';
import ThirdInput from '../components/ThirdInput.vue';
</script>

<template>
    <div class="color-select-view">
        <Header />
        <ThirdInput />
    </div>
</template>

<style scoped>
.color-select-view {
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
</style>