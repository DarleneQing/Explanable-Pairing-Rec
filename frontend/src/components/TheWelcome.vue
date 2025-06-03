<script setup>
// TheWelcome component
import '../assets/base.css';
import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="welcome">
      <h2>Welcome to the application</h2>
  </div>
  <div class="landing-container">
      <RouterLink to="/rec-board" class="start-link">
          <button class="start-button">Start</button>
      </RouterLink>
  </div>
  <div>
    <h3>Test Color Palette</h3>
    <div class="box">
      <div style="background-color: var(--color-master); width: 100px; height: 100px;"></div>
      <div style="background-color: var(--color-value); width: 100px; height: 100px;"></div>
      <div style="background-color: var(--graphical-appearance); width: 100px; height: 100px;"></div>
      <div style="background-color: var(--fabric); width: 100px; height: 100px;"></div>
      <div style="background-color: var(--neckline); width: 100px; height: 100px;"></div>
      <div style="background-color: var(--sleeves); width: 100px; height: 100px;"></div>
      <div style="background-color: var(--length); width: 100px; height: 100px;"></div>
    </div>
    <h3>Item & Blob Color</h3>
    <div class="box">
      <div style="background-color: var(--item-color); width: 100px; height: 100px;"></div>
      <div style="background-color: var(--blobs); width: 100px; height: 100px;"></div>
    </div>
  </div>
</template>

<style scoped>
.welcome {
  margin-top: 200px;
  padding: 2rem;
  text-align: center;
  background-color: var(--window-color1);
  border-radius: 8px;
  margin: 1rem 0;
}

.landing-container {
    padding: 20px;
    margin: 20px;
    border-radius: 8px;
    text-align: center;
}

.start-link {
    text-decoration: none;
}

.start-button {
    background-color: var(--button-color1);
    color: white;
    padding: 15px 30px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.start-button:hover {
    background-color: #588157;
    transform: translateY(-2px);
}

.box{
  display: flex;
  justify-content: flex-start;
}

h2 {
  color: #588157;
}
</style> 