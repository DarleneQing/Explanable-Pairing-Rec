<template>
  <div class="about">
    <h1>About This Project</h1>
    <p>This is the about page of the application.</p>
    <BackendTest />
  </div>
</template>

<script setup>
import BackendTest from '@/components/BackendTest.vue';
</script>

<style>
.about {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}
</style> 