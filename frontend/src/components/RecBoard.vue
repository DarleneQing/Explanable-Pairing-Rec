<script setup>
import '../assets/base.css';
import { ref, onMounted, computed, watch } from 'vue';
import * as d3 from 'd3';
import Filter from './Filter.vue';
import RecScore from './RecScore.vue';
import Comparison from './Comparison.vue';
// State for selected filter categories
const selectedCategories = ref([]);

// State for comparison window visibility
const showComparison = ref(false);

// Position and zoom state
const position = ref({ x: 0, y: 0 });
const zoomValue = ref(25); // Default zoom value (0-100)

// Function to calculate distance between two points
const calculateDistance = (pos1, pos2) => {
  return Math.sqrt(Math.pow(pos1.x - pos2.x, 2) + Math.pow(pos1.y - pos2.y, 2));
};

// Function to generate random position with minimum distance from existing positions
const generateRandomPosition = (existingPositions, minDistance = 200) => {
  let attempts = 0;
  const maxAttempts = 100;
  
  while (attempts < maxAttempts) {
    // Generate position with more spread and ensure it's around center
    const angle = Math.random() * 2 * Math.PI;
    const distance = 100 + Math.random() * 200; // Random distance between 100 and 400 from center
    const x = Math.cos(angle) * distance;
    const y = Math.sin(angle) * distance;
    
    const newPos = { x, y };
    
    // Check if this position is far enough from all existing positions
    const isFarEnough = existingPositions.every(pos => 
      calculateDistance(newPos, pos) >= minDistance
    );
    
    if (isFarEnough) {
      return newPos;
    }
    
    attempts++;
  }
  
  // If we couldn't find a good position after max attempts, return a fallback position
  return {
    x: (Math.random() - 0.5) * 1000,
    y: (Math.random() - 0.5) * 800
  };
};

// Create array of 5 random positions with better spread and minimum distance
const randomPositions = [];
for (let i = 0; i < 5; i++) {
  if (i === 0) {
    randomPositions.push({
      x: (Math.random() - 0.5) * 1000,
      y: (Math.random() - 0.5) * 800
    });
  } else {
    randomPositions.push(generateRandomPosition(randomPositions));
  }
}

// Create array of 5 different blob-shape combinations
const blobShapeCombinations = ref([
  {
    blob: new URL('../assets/blobs/blob-1.svg', import.meta.url).href,
    shape: new URL('../assets/item-shapes/shape-54.svg', import.meta.url).href,
    position: randomPositions[0]
  },
  {
    blob: new URL('../assets/blobs/blob-2.svg', import.meta.url).href,
    shape: new URL('../assets/item-shapes/shape-87.svg', import.meta.url).href,
    position: randomPositions[1]
  },
  {
    blob: new URL('../assets/blobs/blob-3.svg', import.meta.url).href,
    shape: new URL('../assets/item-shapes/shape-72.svg', import.meta.url).href,
    position: randomPositions[2]
  },
  {
    blob: new URL('../assets/blobs/blob-4.svg', import.meta.url).href,
    shape: new URL('../assets/item-shapes/shape-116.svg', import.meta.url).href,
    position: randomPositions[3]
  },
  {
    blob: new URL('../assets/blobs/blob-5.svg', import.meta.url).href,
    shape: new URL('../assets/item-shapes/shape-4.svg', import.meta.url).href,
    position: randomPositions[4]
  }
]);

// Sample data for the bar charts (commented out for now)
// const barChartData = ref([
//   { value: 65, label: 'A', color: 'var(--color-master)' },
//   { value: 45, label: 'B', color: 'var(--color-value)' },
//   { value: 80, label: 'C', color: 'var(--graphical-appearance)' },
//   { value: 30, label: 'D', color: 'var(--fabric)' },
//   { value: 55, label: 'E', color: 'var(--neckline)' },
//   { value: 70, label: 'F', color: 'var(--sleeves)' },
//   { value: 40, label: 'G', color: 'var(--length)' }
// ]);

// Refs for bar chart containers (commented out for now)
// const barChartContainers = ref([]);

// Sample data for the bar charts
const barChartData = ref([
  { value: 65, label: 'A', color: 'var(--color-master)' },
  { value: 45, label: 'B', color: 'var(--color-value)' },
  { value: 80, label: 'C', color: 'var(--graphical-appearance)' },
  { value: 30, label: 'D', color: 'var(--fabric)' },
  { value: 55, label: 'E', color: 'var(--neckline)' },
  { value: 70, label: 'F', color: 'var(--sleeves)' },
  { value: 40, label: 'G', color: 'var(--length)' }
]);

// Refs for bar chart containers
const barChartContainers = ref([]);

// Function to handle filter changes
const handleFilterChange = (categories) => {
  selectedCategories.value = categories;
  console.log('Selected categories:', categories);
  // Here you would typically filter your displayed items based on the selected categories
};

// Functions to handle comparison window
const openComparison = () => {
  showComparison.value = true;
};

const closeComparison = () => {
  showComparison.value = false;
};

// Ref for d3 slider container
const sliderContainer = ref(null);

// Ref for the main content container that will be zoomed
const recBoardContent = ref(null);

// Computed scale transform based on zoom value
const scaleTransform = computed(() => {
  return 0.5 + (zoomValue.value / 100) * 2.2;
});

// Watch for changes to the zoom value and apply the transform
watch([scaleTransform, position], ([newScale, newPosition]) => {
  applyTransform(newScale, newPosition);
});

// Apply transform to the content
const applyTransform = (scale, pos) => {
  if (recBoardContent.value) {
    recBoardContent.value.style.transform = `translate(${pos.x}px, ${pos.y}px) scale(${scale})`;
    recBoardContent.value.style.transformOrigin = 'center center';
  }
};

// Function to create bar chart (commented out for now)
// const createBarChart = (container) => {
//   if (!container) return;
//   
//   const margin = { top: 10, right: 10, bottom: 10, left: 10 };
//   const width = 120 - margin.left - margin.right;
//   const height = 90 - margin.top - margin.bottom;

//   // Clear any existing content
//   d3.select(container).selectAll('*').remove();

//   const svg = d3.select(container)
//     .append('svg')
//     .attr('width', width + margin.left + margin.right)
//     .attr('height', height + margin.top + margin.bottom)
//     .append('g')
//     .attr('transform', `translate(${margin.left},${margin.top})`);

//   const y = d3.scaleBand()
//     .range([0, height])
//     .domain(barChartData.value.map(d => d.label))
//     .padding(0.2);

//   const x = d3.scaleLinear()
//     .range([0, width])
//     .domain([0, 100]);

//   svg.selectAll('.bar')
//     .data(barChartData.value)
//     .enter()
//     .append('rect')
//     .attr('class', 'bar')
//     .attr('y', d => y(d.label))
//     .attr('height', y.bandwidth())
//     .attr('x', 0)
//     .attr('width', d => x(d.value))
//     .attr('fill', d => d.color);
// };

// Function to create bar chart
const createBarChart = (container) => {
  if (!container) return;
  
  const margin = { top: 10, right: 10, bottom: 10, left: 10 };
  const width = 120 - margin.left - margin.right;
  const height = 90 - margin.top - margin.bottom;

  // Clear any existing content
  d3.select(container).selectAll('*').remove();

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const y = d3.scaleBand()
    .range([0, height])
    .domain(barChartData.value.map(d => d.label))
    .padding(0.2);

  const x = d3.scaleLinear()
    .range([0, width])
    .domain([0, 100]);

  svg.selectAll('.bar')
    .data(barChartData.value)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('y', d => y(d.label))
    .attr('height', y.bandwidth())
    .attr('x', 0)
    .attr('width', d => x(d.value))
    .attr('fill', d => d.color);
};

// Setup D3 bar chart and drag behavior
onMounted(() => {
  // Initialize the transform with default zoom level
  applyTransform(scaleTransform.value, position.value);
  
  // Setup drag behavior for the content
  if (recBoardContent.value) {
    const drag = d3.drag()
      .on('start', () => {
        d3.select(recBoardContent.value).style('transition', 'none');
      })
      .on('drag', (event) => {
        position.value = {
          x: position.value.x + event.dx,
          y: position.value.y + event.dy
        };
        applyTransform(scaleTransform.value, position.value);
      })
      .on('end', () => {
        d3.select(recBoardContent.value).style('transition', 'transform 0.2s ease');
      });

    d3.select(recBoardContent.value)
      .call(drag)
      .style('cursor', 'move');
  }

  // Create bar charts after a short delay to ensure containers are mounted (commented out for now)
  // setTimeout(() => {
  //   barChartContainers.value.forEach(container => {
  //     createBarChart(container);
  //   });
  // }, 100);

  // Create bar charts after a short delay to ensure containers are mounted
  setTimeout(() => {
    barChartContainers.value.forEach(container => {
      createBarChart(container);
    });
  }, 100);

  // Existing slider setup code
  if (sliderContainer.value) {
    const height = 180;
    const margin = { top: 10, right: 10, bottom: 10, left: 10 };
    
    // Create SVG
    const svg = d3.select(sliderContainer.value)
      .append('svg')
      .attr('width', 50)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Create scale
    const scale = d3.scaleLinear()
      .domain([0, 100])
      .range([height, 0])
      .clamp(true);
    
    // Create slider
    const slider = svg.append('g')
      .attr('class', 'slider')
      .attr('transform', `translate(15,0)`);
    
    // Add track
    slider.append('line')
      .attr('class', 'track')
      .attr('y1', scale.range()[0])
      .attr('y2', scale.range()[1])
      .attr('stroke', '#ccc')
      .attr('stroke-width', 8)
      .attr('stroke-linecap', 'round');
    
    // Add track overlay
    slider.append('line')
      .attr('class', 'track-overlay')
      .attr('y1', scale.range()[0])
      .attr('y2', scale.range()[1])
      .attr('stroke', 'transparent')
      .attr('stroke-width', 30)
      .attr('stroke-linecap', 'round')
      .attr('cursor', 'pointer')
      .call(d3.drag()
        .on('start.interrupt', function() { slider.interrupt(); })
        .on('start drag', function(event) {
          zoomValue.value = Math.round(scale.invert(event.y));
          updateHandle(zoomValue.value);
          applyTransform(scaleTransform.value, position.value);
        }));
    
    // Add ticks
    slider.insert('g', '.track-overlay')
      .attr('class', 'ticks')
      .selectAll('text')
      .data([0, 25, 50, 75, 100])
      .enter()
      .append('text')
      .attr('x', -15)
      .attr('y', scale)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .text(d => d);
    
    // Add handle
    const handle = slider.append('circle')
      .attr('class', 'handle')
      .attr('r', 10)
      .attr('fill', 'var(--button-color1)')
      .attr('cursor', 'pointer')
      .attr('cy', scale(zoomValue.value))
      .call(d3.drag()
        .on('start.interrupt', function() { slider.interrupt(); })
        .on('start drag', function(event) {
          zoomValue.value = Math.round(scale.invert(event.y));
          updateHandle(zoomValue.value);
          applyTransform(scaleTransform.value, position.value);
        }));
    
    // Update handle position
    function updateHandle(value) {
      handle.attr('cy', scale(value));
    }
  }
});

// Function to get current zoom level
const getZoomLevel = () => {
  return zoomValue.value;
};
</script>

<template>
  <div class="rec-board">
    <!-- Fixed elements that don't zoom -->
    <div class="fixed-elements">
      <div ref="sliderContainer" class="zoom-slider-container">
        <div class="zoom-label">Zoom</div>
      </div>
      
      <Filter @filter-changed="handleFilterChange" />
      
      <div class="rec-score-container">
        <RecScore />
      </div>
    </div>
    
    <!-- Zoomable and draggable content container -->
    <div ref="recBoardContent" class="rec-board-content">
      <div class="content-wrapper">
        <div v-for="(combination, index) in blobShapeCombinations" 
             :key="index" 
             class="content-item"
             :style="{ transform: `translate(${combination.position.x}px, ${combination.position.y}px)` }">
          <div class="svg-hover-wrapper">
            <img :src="combination.blob" class="blob-svg" alt="Blob background" @click="openComparison" />
            <img :src="combination.shape" class="shape-svg" alt="Shape overlay"  @click="openComparison" />
          </div>
          <!-- Bar chart container commented out for now -->
          <!-- <div :ref="el => { if(el) barChartContainers[index] = el }" class="bar-chart-container"></div> -->
          <div :ref="el => { if(el) barChartContainers[index] = el }" class="bar-chart-container"></div>
        </div>
      </div>
    </div>
    <!-- Comparison component - conditionally rendered -->
    <Comparison v-if="showComparison" @close="closeComparison" />
  </div>
</template>

<style scoped>
.rec-board {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.fixed-elements {
  position: fixed;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1000;
}

.fixed-elements > * {
  pointer-events: auto;
}

.rec-board-content {
  position: absolute;
  width: 100vw;
  height: 100vh;
  transition: transform 0.2s ease;
  transform-origin: center center;
  user-select: none;
  touch-action: none;
}

/* Zoom slider styles */
.zoom-slider-container {
  position: fixed;
  bottom: 20px;
  left: 20px;
  background-color: #ffffffcc;
  border-radius: 8px;
  padding: 5px;
  box-shadow: 0 2px 5px #0000001a;
}

.zoom-label {
  text-align: center;
  font-size: 12px;
  margin-bottom: 5px;
  color: #666;
  font-weight: bold;
}

.slider .track-overlay {
  cursor: pointer;
}

.slider .handle {
  stroke: #fff;
  stroke-width: 1.5px;
  transition: fill 0.3s ease;
}

.slider .handle:hover {
  fill: var(--button-color2);
}

.slider text {
  fill: #666;
}

.rec-score-container {
  position: fixed;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #588157;
  border-radius: 20px;
  padding: 5px;
}

.content-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content-item {
  position: absolute;
  width: 300px;
  height: 300px;
  transform-origin: center center;
}

.svg-hover-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 150px;
  height: 150px;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.svg-hover-wrapper:hover {
  transform: translate(-50%, -50%) scale(1.05);
  opacity: 0.8;
}

.shape-svg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: auto;
  margin-right: -20px;
  z-index: 2;
  cursor: pointer;
}

.bar-chart-container {
  position: absolute;
  left: calc(50% + 30px);
  top: 45%;
  transform: translateY(-50%);
  width: auto;
  height: 60px;
  z-index: 1;
}

.blob-svg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 150px;
  height: auto;
  z-index: 1;
  cursor: pointer;
}

.bar {
  transition: fill 0.3s ease;
}

.bar:hover {
  opacity: 0.8;
}
</style> 