<script setup lang="ts">
import Header from '../components/Header.vue';
import SecondInput from '../components/SecondInput.vue';
</script>

<template>
    <div class="type-select-view">
        <Header />
        <SecondInput />
    </div>
</template>

<style scoped>
.type-select-view {
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
</style>