<template>
  <div class="filter-wrapper" :class="{ minimized: isMinimized }">
    <div v-if="isMinimized" class="filter-header">
      <p>Filters</p>
      <div class="control-icon" @click="isMinimized = !isMinimized">
        <img src="@/components/icons/maximize-icon.svg" alt="Maximize" width="20" height="20" class="icon" />
      </div>
    </div>
    <div v-else class="filter-container">
      <div class="filter-title-row">
        <h3>Filter by Category</h3>
        <div class="control-icon" @click="isMinimized = !isMinimized">
          <img src="@/components/icons/minimize-icon.svg" alt="Minimize" width="18" height="18" class="icon" />
        </div>
      </div>
      <div class="filter-buttons" ref="buttonContainer"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import * as d3 from 'd3';
import '../assets/base.css';

const buttonContainer = ref(null);
const selectedCategories = ref([]);
const isMinimized = ref(true);

const categories = [
  'Jersey Basic', 'Jersey Fancy', 'Accessories', 'Shoes', 'Knitwear',
  'Shirts', 'Trousers', 'Dressed', 'Shorts', 'Dresses Ladies',
  'Trousers Denim', 'Skirts', 'Special Offers', 'Blouses'
];

const renderButtons = () => {
  if (!buttonContainer.value) return;
  
  const container = d3.select(buttonContainer.value);
  
  // Clear existing buttons
  container.selectAll('*').remove();
  
  // Create buttons for each category using D3
  container.selectAll('.filter-button')
    .data(categories)
    .enter()
    .append('button')
    .attr('class', 'filter-button')
    .style('padding', '0.3rem 0.6rem')
    .style('border-radius', '15px')
    .style('background-color', d => selectedCategories.value.includes(d) ? 'var(--button-color1)' : 'var(--window-color1)')
    .style('border', '1px solid')
    .style('border-color', d => selectedCategories.value.includes(d) ? 'var(--button-color1)' : 'var(--window-color1)')
    .style('cursor', 'pointer')
    .style('transition', 'all 0.2s ease')
    .style('font-size', '0.7rem')
    .style('color', d => selectedCategories.value.includes(d) ? 'white' : 'var(--font-color1)')
    .style('box-shadow', d => selectedCategories.value.includes(d) 
      ? '0 2px 4px rgba(150, 86, 162, 0.3)' 
      : '0 2px 4px rgba(0, 0, 0, 0.1)')
    .text(d => d)
    .on('mouseover', function(event, d) {
      d3.select(this)
        .style('transform', 'translateY(-2px)')
        .style('box-shadow', '0 4px 8px rgba(0, 0, 0, 0.15)')
    })
    .on('mouseout', function(event, d) {
      d3.select(this)
        .style('transform', 'translateY(0)')
    })
    .on('click', (event, d) => {
      toggleCategory(d);
    });
};

const toggleCategory = (category) => {
  if (selectedCategories.value.includes(category)) {
    selectedCategories.value = selectedCategories.value.filter(cat => cat !== category);
  } else {
    selectedCategories.value.push(category);
  }
  
  // Update the UI
  renderButtons();
  
  // Emit event to parent component
  emit('filter-changed', selectedCategories.value);
};

// Watch for changes to isMinimized and render buttons when expanded
watch(isMinimized, async (newValue) => {
  if (!newValue) {
    // Component is being expanded, wait for DOM update then render buttons
    await nextTick();
    renderButtons();
  }
});

const emit = defineEmits(['filter-changed']);

onMounted(() => {
  // Only render buttons if component starts expanded
  if (!isMinimized.value) {
    renderButtons();
  }
});
</script>

<style scoped>
.filter-wrapper {
  position: fixed;
  bottom: 10px;
  right: 10px;
  max-width: 300px;
  width: auto;
  background-color: var(--window-color3);
  padding: 10px;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.filter-wrapper.minimized {
  padding: 5px 10px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.filter-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.filter-header p {
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
  border-radius: 4px;
  transition: background-color 0.2s ease;
  margin-left: 10px;
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

h3 {
  color: white;
  font-size: 1rem;
  font-weight: bold;
}

.filter-container {
  margin: 0;
  padding: 0;
  border-radius: 0;
  background-color: transparent;
  max-width: 300px;
  width: auto;
  min-height: auto;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
  align-items: center;
  justify-content: center;
}

.filter-button {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background-color: var(--window-color4);
  border: 2px solid var(--window-color4);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  color: var(--font-color1);
  box-shadow: 0 2px 4px #0000001a;
}

.filter-button:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  border-color: #4a90e2;
}

.filter-button.selected {
  background-color: #4a90e2;
  color: white;
  border-color: #4a90e2;
  box-shadow: 0 2px 4px rgba(74, 144, 226, 0.3);
}
</style>
