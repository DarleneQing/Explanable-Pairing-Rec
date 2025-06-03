<script setup>
import RecBoard from '../components/RecBoard.vue'
import '../assets/base.css'
import Instruction from '../components/Instruction.vue'
import { ref } from 'vue'

// State for showing/hiding instructions
const showInstructions = ref(false);
// State for maximizing/minimizing the input item
const isMinimized = ref(true);
</script>

<template>
  <div class="main-rec-view">
    <div class="header">
      <div class="input-item" :class="{ minimized: isMinimized }">
        <div class="input-header">
          <p>Query Item</p>
          <div class="control-icon" @click="isMinimized = !isMinimized">
            <img v-if="!isMinimized" src="@/components/icons/minimize-icon.svg" alt="Minimize" width="20" height="20" class="icon" />
            <img v-else src="@/components/icons/maximize-icon.svg" alt="Maximize" width="20" height="20" class="icon" />
          </div>
        </div>
        <div class="query-shape-container">
          <img v-if="isMinimized" src="@assets/item-shapes/shape-22.svg" alt="query shape" class="item-shape" />
        </div>
        <img v-if="!isMinimized" src="@assets/images/052/0529180002.jpg" alt="query image" class="query-image" />
      </div>
      <h1>Pairing Recommender</h1>
      <div class="question-circle" @click="showInstructions = true">
        <img src="@/components/icons/question-circle.svg" alt="Question Circle Icon" width="50" height="50" class="question-icon" />
      </div>
    </div>
    <div class="content-container">
      <RecBoard />
    </div>
    <div v-if="showInstructions" class="instruction-overlay">
      <div class="instruction-container">
        <Instruction />
        <button class="close-button" @click="showInstructions = false">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-rec-view {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

.input-item {
  position: fixed;
  top: 5px;
  left: 10px;
  z-index: 1001;
  background-color: var(--button-color1);
  padding: 10px;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.input-item.minimized {
  padding: 5px 10px;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.input-item p {
  color: white;
  font-size: 1rem;
  font-weight: bold;
  margin: 0;
}

.control-icon {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10px;
  padding: 2px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.query-shape-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.control-icon:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.icon {
  filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%);
  transition: transform 0.2s ease;
}

.control-icon:hover .icon {
  transform: scale(1.1);
}

.query-image {
  width: auto;
  height: 180px;
}

.item-shape {
  width: auto;
  height: 50px;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1001;
  background-color: none;
  padding: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

h1 {
  color: var(--button-color1);
  text-align: center;
  margin: 0;
}

.content-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.question-circle {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 50px;
  height: 50px;
  cursor: pointer;
}

.question-icon {
  filter: invert(42%) sepia(13%) saturate(1188%) hue-rotate(78deg) brightness(92%) contrast(86%);
  transition: transform 0.3s ease, filter 0.3s ease;
}

.question-icon:hover {
  transform: scale(1.1);
}

.instruction-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.instruction-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 80%;
  max-height: 80%;
  overflow-y: auto;
  position: relative;
}

.close-button {
  margin-top: 15px;
  padding: 8px 16px;
  background-color: var(--button-color1);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.close-button:hover {
  background-color: #588157;
}
</style>

