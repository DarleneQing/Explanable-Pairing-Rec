<script setup lang="ts">
import Header from '../components/Header.vue';
import ForthInput from '../components/ForthInput.vue';
</script>

<template>
    <div class="appearance-select-view">
        <Header />
        <ForthInput />
    </div>
</template>

<style scoped>
.appearance-select-view {
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
</style>