<template>
    <WindowLayout>
        <template #header>
            <h1 class="explain-title">How it works?</h1>
            <div class="explain-subtitle">Discover meaningful connections through HeteroGraph Attention Networks</div>
        </template>
        
        <template #content>
            <div class="explain-description">
                <p class="main-description">
                    Our platform leverages HeteroGraph Attention Networks to create intelligent pairing recommendations. 
                    By analyzing complex relationships between items and incorporating human-centric data principles, 
                    we provide transparent, explainable suggestions that help you understand the reasoning behind each match.
                </p>
                
                <div class="features-grid">
                    <div class="feature-item">
                        <div class="feature-icon" style="background-color: var(--brand-primary);">🔍</div>
                        <h3>HeteroGraph Analysis</h3>
                        <p>Advanced graph neural networks that understand complex relationships between different types of items, creating more meaningful connections.</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon" style="background-color: var(--ui-interactive-brown);">🧠</div>
                        <h3>Attention Mechanism</h3>
                        <p>Intelligent weighting system that focuses on the most relevant features and relationships for each recommendation.</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon" style="background-color: var(--ui-interactive);">📊</div>
                        <h3>Data Humanism</h3>
                        <p>Human-centric approach to data analysis that ensures recommendations are meaningful, ethical, and aligned with human values.</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon" style="background-color: var(--brand-secondary);">🎯</div>
                        <h3>Explainable AI</h3>
                        <p>Transparent reasoning behind each recommendation, helping you understand why items are suggested together.</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon" style="background-color: var(--ui-interactive-light);">📈</div>
                        <h3>Visual Insights</h3>
                        <p>Interactive visualizations that make complex relationships and patterns easy to understand and explore.</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon" style="background-color: var(--ui-success);">🤝</div>
                        <h3>Human-AI Collaboration</h3>
                        <p>Seamless integration of human expertise and AI capabilities for more meaningful and trustworthy recommendations.</p>
                    </div>
                </div>
                
                <div class="additional-content">
                    <h2>Why Choose Our Platform?</h2>
                    <p>
                        Our platform goes beyond traditional recommendation systems by combining cutting-edge HeteroGraph 
                        Attention Networks with principles of data humanism. We believe that the best recommendations 
                        come from understanding both the technical relationships between items and the human context 
                        in which they exist.
                    </p>
                    <p>
                        Through our innovative approach, we provide not just recommendations, but meaningful insights 
                        into why items work well together. Our visual explanations help you understand the complex 
                        relationships and patterns that influence each suggestion, making the decision-making process 
                        more transparent and trustworthy.
                    </p>
                </div>
            </div>
        </template>
        
        <template #actions>
            <button class="primary-button" @click="goToBegin">Let's Get Started!</button>
        </template>
    </WindowLayout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import WindowLayout from './WindowLayout.vue'

const router = useRouter()

const goToBegin = () => {
    router.push('/begin')
}
</script>

<style scoped>
.explain-title {
    font-size: var(--font-size-2xl);
    font-weight: var(--font-weight-bold);
    color: var(--brand-primary);
    margin: 0 0 var(--space-sm) 0;
    letter-spacing: -0.02em;
    text-shadow: 0 1px 2px rgba(var(--ui-text-primary-rgb), 0.1);
}

.explain-subtitle {
    font-size: var(--font-size-md);
    color: var(--text-secondary);
    font-weight: var(--font-weight-medium);
}

.explain-description {
    padding-bottom: var(--space-xl);
}

.main-description {
    font-size: var(--font-size-sm);
    color: var(--text-primary);
    line-height: var(--line-height-relaxed);
    text-align: center;
    margin-bottom: var(--space-2xl);
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: var(--space-lg);
    margin-bottom: var(--space-2xl);
}

.feature-item {
    text-align: center;
    padding: var(--space-lg);
    background: rgba(255, 255, 255, 0.5);
    border-radius: var(--border-radius-lg);
    border: var(--border-width-thin) solid var(--border-light);
    transition: var(--transition-all);
}

.feature-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    background: rgba(255, 255, 255, 0.8);
}

.feature-icon {
    width: 40px;
    height: 40px;
    border-radius: var(--border-radius-full);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--font-size-lg);
    margin: 0 auto var(--space-sm) auto;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.feature-item h3 {
    font-size: var(--font-size-md);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    margin: 0 0 var(--space-xs) 0;
}

.feature-item p {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
    margin: 0;
    line-height: var(--line-height-normal);
}

.additional-content {
    margin-top: var(--space-2xl);
    padding: var(--space-xl);
    background: rgba(255, 255, 255, 0.3);
    border-radius: var(--border-radius-lg);
    border: var(--border-width-thin) solid var(--border-light);
}

.additional-content h2 {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-bold);
    color: var(--brand-primary);
    margin: 0 0 var(--space-md) 0;
    text-align: center;
}

.additional-content p {
    font-size: var(--font-size-xs);
    color: var(--text-primary);
    line-height: var(--line-height-normal);
    margin-bottom: var(--space-md);
    text-align: left;
}

.additional-content p:last-child {
    margin-bottom: 0;
}

.primary-button {
    background: linear-gradient(135deg, var(--ui-interactive) 0%, var(--ui-interactive-brown) 100%);
    color: var(--text-inverse);
    padding: var(--space-md) var(--space-xl);
    border: none;
    border-radius: var(--border-radius-lg);
    cursor: pointer;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    box-shadow: 
        0 4px 12px rgba(var(--ui-interactive-rgb), 0.3),
        0 2px 4px rgba(var(--ui-text-primary-rgb), 0.1);
    transition: var(--transition-all);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(var(--ui-interactive-rgb), 0.5);
}

.primary-button:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 6px 20px rgba(var(--ui-interactive-rgb), 0.4),
        0 4px 8px rgba(var(--ui-text-primary-rgb), 0.15);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
}

.primary-button:active {
    transform: translateY(0);
}

/* Responsive design for content-specific elements */
@media (max-width: 768px) {
    .explain-title {
        font-size: var(--font-size-xl);
    }
    
    .features-grid {
        grid-template-columns: 1fr;
        gap: var(--space-md);
    }
    
    .primary-button {
        width: 100%;
        text-align: center;
    }
}

@media (max-width: 480px) {
    .explain-title {
        font-size: var(--font-size-lg);
    }
    
    .explain-subtitle {
        font-size: var(--font-size-sm);
    }
    
    .main-description {
        font-size: var(--font-size-xs);
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
}
</style>

