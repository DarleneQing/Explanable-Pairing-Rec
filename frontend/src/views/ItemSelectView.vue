<script setup lang="ts">
import Header from '../components/Header.vue';
import ItemInput from '../components/ItemInput.vue';
</script>

<template>
    <div class="item-select-view">
        <Header />
        <ItemInput />
    </div>
</template>

<style scoped>
.item-select-view {
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
</style>