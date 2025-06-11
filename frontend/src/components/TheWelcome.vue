<script setup>
// TheWelcome component
import '../assets/base.css';
import { RouterLink, useRouter } from 'vue-router';
import { onMounted } from 'vue';
import BackendTest from './BackendTest.vue';
import { useSessionStore } from '../stores/session';

const sessionStore = useSessionStore();
const router = useRouter();

// Load any existing session data when component mounts
onMounted(async () => {
  await sessionStore.loadStoredSession();
});

const handleStartClick = async () => {
  try {
    // Only create a new session if one doesn't exist
    if (!sessionStore.session) {
      await sessionStore.createSession();
      console.log('Session created successfully:', sessionStore.session);
    }
    // Navigate to first-input page to collect user data
    router.push('/how-it-works');
  } catch (error) {
    console.error('Failed to create session:', error);
    // You might want to show an error message to the user
  }
};
</script>

<template>
  <div class="welcome">
      <h2>Welcome to the application</h2>
  </div>
  <div class="landing-container">
      <button @click="handleStartClick" class="start-button">Start</button>
  </div>
  <BackendTest />
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
    background-color: var(--window-color3);
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