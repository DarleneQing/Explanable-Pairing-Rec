<script setup lang="ts">
import { Item } from '../types/item';
import { Rec } from '../types/Rec';

// Define emits
const emit = defineEmits<{
  close: []
}>();

// Get the two item instances
const item1 = Item.ITEM_529180002;
const item2 = Item.ITEM_830185001;
const rec1 = Rec.RECS1;
// Create an array of items to avoid duplication in template
const items = [item1, item2];

// Function to handle close button click
const handleClose = () => {
  emit('close');
};

// Function to get recommendation score for a given attribute and item
const getRecScore = (item: Item, attribute: string): number | null => {
  // Only show scores for item2 (ITEM_830185001) since rec1 corresponds to it
  if (item.article_id !== item2.article_id) {
    return null;
  }
  
  switch (attribute) {
    case 'color':
      return rec1.color_importance;
    case 'luminance':
      return rec1.luminance_importance;
    case 'appearance':
      return rec1.appearance_importance;
    case 'fabric':
      return rec1.fabric_importance;
    case 'neckline':
      return rec1.neckline_importance;
    case 'sleeve':
      return rec1.sleeve_importance;
    case 'length':
      return rec1.length_importance;
    default:
      return null;
  }
};
</script>

<template>
    <div class="comparison-overlay">
        <div class="comparison-container">
            <div class="header">
                <h3>Item Comparison</h3>
                <button class="close-btn" aria-label="Close" @click="handleClose">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
            </div>
            
            <div class="comparison-content">
                <div class="compare-section">
                    <div class="image-comparison">
                        <div class="image-container">
                            <img src="@assets/images/052/0529180002.jpg" alt="Item 1" class="compare-image"/>
                        </div>
                        
                        <div class="compatibility-score">
                            <div class="score-label">Compatibility Score</div>
                            <div class="score-value">0.8534</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: 85.34%"></div>
                            </div>
                        </div>
                        
                        <div class="image-container">
                            <img src="@assets/images/083/0830185001.jpg" alt="Item 2" class="compare-image"/>
                        </div>
                    </div>
                </div>

                <div class="details-section">
                    <div class="item-cards">
                        <div v-for="(item, index) in items" :key="index" class="item-card">
                            <h4>{{ item.prod_name }}</h4>
                            <div class="attributes-grid">
                                <div class="attribute">
                                    <span class="attribute-label">Color</span>
                                    <div class="attribute-content">
                                        <span class="attribute-value">{{ item.perceived_colour_master_name }}</span>
                                        <span v-if="getRecScore(item, 'color')" class="importance-score">
                                            {{ (getRecScore(item, 'color')! * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                                <div class="attribute">
                                    <span class="attribute-label">Luminance</span>
                                    <div class="attribute-content">
                                        <span class="attribute-value">{{ item.perceived_colour_value_name }}</span>
                                        <span v-if="getRecScore(item, 'luminance')" class="importance-score">
                                            {{ (getRecScore(item, 'luminance')! * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                                <div class="attribute">
                                    <span class="attribute-label">Appearance</span>
                                    <div class="attribute-content">
                                        <span class="attribute-value">{{ item.graphical_appearance_name }}</span>
                                        <span v-if="getRecScore(item, 'appearance')" class="importance-score">
                                            {{ (getRecScore(item, 'appearance')! * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                                <div class="attribute">
                                    <span class="attribute-label">Neckline</span>
                                    <div class="attribute-content">
                                        <span class="attribute-value">{{ item.neckline_prediction }}</span>
                                        <span v-if="getRecScore(item, 'neckline')" class="importance-score">
                                            {{ (getRecScore(item, 'neckline')! * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                                <div class="attribute">
                                    <span class="attribute-label">Sleeve</span>
                                    <div class="attribute-content">
                                        <span class="attribute-value">{{ item.sleeve_prediction }}</span>
                                        <span v-if="getRecScore(item, 'sleeve')" class="importance-score">
                                            {{ (getRecScore(item, 'sleeve')! * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                                <div class="attribute">
                                    <span class="attribute-label">Length</span>
                                    <div class="attribute-content">
                                        <span class="attribute-value">{{ item.length_prediction }}</span>
                                        <span v-if="getRecScore(item, 'length')" class="importance-score">
                                            {{ (getRecScore(item, 'length')! * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                                <div class="attribute">
                                    <span class="attribute-label">Fabric</span>
                                    <div class="attribute-content">
                                        <span class="attribute-value">{{ item.detected_fabrics }}</span>
                                        <span v-if="getRecScore(item, 'fabric')" class="importance-score">
                                            {{ (getRecScore(item, 'fabric')! * 100).toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.comparison-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(54, 55, 55, 0.4);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1001;
    padding: 1.5rem;
    z-index: 1009;
}

.comparison-container {
    background: var(--main-background);
    border-radius: 12px;
    border: 1px solid var(--window-color1);
    box-shadow: 
        0 8px 32px rgba(54, 55, 55, 0.1),
        0 2px 8px rgba(54, 55, 55, 0.05);
    max-width: 85vw;
    max-height: 85vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background: var(--button-color1);
    color: white;
    border-bottom: 1px solid var(--window-color1);
}

h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    color: white;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 6px;
    transition: background-color 0.2s ease;
    opacity: 0.8;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.15);
    opacity: 1;
}

.comparison-content {
    padding: 1.5rem;
    overflow-y: auto;
    flex: 1;
    background: var(--main-background);
}

.compare-section {
    margin-bottom: 1.5rem;
}

.image-comparison {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
}

.image-container {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(54, 55, 55, 0.1);
    transition: transform 0.2s ease;
    background: white;
}

.image-container:hover {
    transform: translateY(-2px);
}

.compare-image {
    width: 100px;
    height: 130px;
    object-fit: cover;
    display: block;
}

.compatibility-score {
    text-align: center;
    padding: 1.25rem;
    background: var(--window-color1);
    border-radius: 10px;
    border: 1px solid var(--window-color2);
    min-width: 160px;
}

.score-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--font-color1);
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.score-value {
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    color: var(--item-color);
}

.score-bar {
    background: var(--window-color2);
    border-radius: 6px;
    height: 6px;
    overflow: hidden;
}

.score-fill {
    background: var(--button-color1);
    height: 100%;
    border-radius: 6px;
    transition: width 0.6s ease;
}

.details-section {
    border-top: 1px solid var(--window-color1);
    padding-top: 1.5rem;
}

.item-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

.item-card {
    background: white;
    border: 1px solid var(--window-color1);
    border-radius: 10px;
    padding: 1.25rem;
    box-shadow: 0 2px 8px rgba(54, 55, 55, 0.05);
}

h4 {
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: var(--item-color);
    text-align: center;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--window-color1);
}

.attributes-grid {
    display: grid;
    gap: 0.75rem;
}

.attribute {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--window-color2);
}

.attribute:last-child {
    border-bottom: none;
}

.attribute-label {
    font-weight: 500;
    color: var(--font-color1);
    font-size: 0.8rem;
    text-transform: capitalize;
    flex-shrink: 0;
    margin-right: 1rem;
    min-width: 80px;
}

.attribute-content {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    text-align: right;
}

.attribute-value {
    font-weight: 400;
    color: var(--item-color);
    font-size: 0.8rem;
    line-height: 1.3;
}

.importance-score {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--button-color1);
    background: rgba(var(--button-color1-rgb, 76, 175, 80), 0.1);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    border: 1px solid rgba(var(--button-color1-rgb, 76, 175, 80), 0.2);
}

/* Responsive design */
@media (max-width: 768px) {
    .comparison-overlay {
        padding: 1rem;
    }
    
    .header {
        padding: 1rem 1.25rem;
    }
    
    h3 {
        font-size: 1.125rem;
    }
    
    .comparison-content {
        padding: 1.25rem;
    }
    
    .image-comparison {
        flex-direction: column;
        gap: 1.25rem;
    }
    
    .item-cards {
        grid-template-columns: 1fr;
        gap: 1.25rem;
    }
    
    .attribute {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.25rem;
    }
    
    .attribute-label {
        min-width: auto;
    }
    
    .attribute-content {
        text-align: left;
        width: 100%;
    }
    
    .attribute-value {
        text-align: left;
    }
}

@media (max-width: 480px) {
    .compare-image {
        width: 90px;
        height: 120px;
    }
    
    .compatibility-score {
        padding: 1rem;
        min-width: 140px;
    }
    
    .score-value {
        font-size: 1.5rem;
    }
}
</style>