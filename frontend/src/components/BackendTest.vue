<template>
  <div class="backend-test">
    <h2>Backend Connection Test</h2>
    <button @click="testBackendConnection">Test Connection</button>
    <div v-if="response" class="response">
      <h3>Response from Backend:</h3>
      <pre>{{ response }}</pre>
    </div>
    <div v-if="error" class="error">
      <h3>Error:</h3>
      <pre>{{ error }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const response = ref(null);
const error = ref(null);

async function testBackendConnection() {
  try {
    response.value = null;
    error.value = null;
    
    console.log('Attempting to connect to backend at: http://localhost:8000/api/test');
    const res = await fetch('http://localhost:8000/api/test');
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    
    const data = await res.json();
    response.value = data;
    console.log('Received response:', data);
  } catch (err) {
    error.value = `Error: ${err.message}. Please check browser console for more details.`;
    console.error('Error connecting to backend:', err);
  }
}
</script>

<style scoped>
.backend-test {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
}

button:hover {
  background-color: #45a049;
}

.response {
  background-color: #f0f8ff;
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
}

.error {
  background-color: #ffebee;
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
  color: #d32f2f;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style> 