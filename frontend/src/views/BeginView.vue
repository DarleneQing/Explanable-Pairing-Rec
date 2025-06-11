<script setup lang="ts">
import Header from '../components/Header.vue';
import FirstInput from '../components/FirstInput.vue';
</script>

<template>
    <div class="begin-view">
        <Header />
        <FirstInput />
    </div>
</template>

<style scoped>
.begin-view {
    height: 100vh;
    overflow: hidden;
    display: flex;

    flex-direction: column;
}
</style>
