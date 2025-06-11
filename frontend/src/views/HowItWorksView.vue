<script setup lang="ts">
import Header from '../components/Header.vue';
import Explain from '../components/Explain.vue';
</script>

<template>
    <div class="how-it-works-view">
        <Header />
        <Explain />
    </div>
</template>

<style scoped>
.how-it-works-view {
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
</style>
