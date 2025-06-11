<template>
    <header class="header-container">
        <div class="header-content">
            <div class="header-brand">
                <div class="brand-icon">
                    <div class="icon-gradient"></div>
                </div>
                <div class="brand-text">
                    <h1 class="header-title">PairSynergy</h1>
                    <span class="header-tagline">Explanable Fashion Recommender</span>
                </div>
            </div>
            <div class="header-accent"></div>
        </div>
    </header>
</template>

<style scoped>
.header-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: var(--space-lg) var(--space-2xl);
    background: linear-gradient(135deg, var(--window-color1) 0%, var(--window-color2) 100%);
    backdrop-filter: blur(20px) saturate(180%);
    border-bottom: var(--border-width-thin) solid rgba(var(--ui-interactive-rgb), 0.2);
    position: sticky;
    top: 0;
    z-index: var(--z-sticky);
    transition: var(--transition-all);
    box-shadow: 0 1px 20px rgba(var(--brand-primary-rgb), 0.08);
}

.header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        135deg, 
        rgba(var(--brand-primary-rgb), 0.03) 0%, 
        rgba(var(--ui-interactive-brown-rgb), 0.03) 50%,
        rgba(var(--ui-interactive-rgb), 0.03) 100%
    );
    z-index: -1;
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 1200px;
    width: 100%;
    position: relative;
}

.header-brand {
    display: flex;
    align-items: center;
    gap: var(--space-md);
    position: relative;
}

.brand-icon {
    position: relative;
    width: 45px;
    height: 45px;
    border-radius: var(--border-radius-xl);
    background: linear-gradient(135deg, var(--ui-interactive) 0%, var(--ui-interactive-brown) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 
        0 4px 15px rgba(var(--ui-interactive-rgb), 0.3),
        0 1px 3px rgba(var(--brand-primary-rgb), 0.1);
    transition: var(--transition-all);
    overflow: hidden;
}

.brand-icon::before {
    content: '👗';
    font-size: var(--font-size-lg);
    z-index: 2;
    position: relative;
}

.icon-gradient {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(
        45deg,
        transparent 30%,
        rgba(var(--ui-interactive-brown-rgb), 0.4) 50%,
        transparent 70%
    );
    transform: rotate(-45deg);
    transition: var(--transition-slow);
}

.brand-icon:hover {
    transform: translateY(-2px) scale(1.05);
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
    box-shadow: 
        0 6px 25px rgba(var(--brand-primary-rgb), 0.4),
        0 2px 8px rgba(var(--ui-interactive-rgb), 0.15);
}

.brand-icon:hover .icon-gradient {
    transform: rotate(-45deg) translateX(100%);
}

.brand-text {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
}

.header-title {
    font-size: var(--font-size-2xl);
    font-weight: var(--font-weight-bold);
    color: var(--brand-primary);
    margin: 0;
    letter-spacing: -0.025em;
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    transition: var(--transition-colors);
    position: relative;
}

.header-title::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--brand-primary), var(--brand-secondary));
    transition: width 0.3s ease;
}

.header-brand:hover .header-title::after {
    width: 100%;
}

.header-tagline {
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-medium);
    color: var(--ui-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0.8;
    transition: var(--transition-colors);
}

.header-brand:hover .header-tagline {
    opacity: 1;
    color: var(--ui-interactive-brown);
}

.header-accent {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, var(--brand-primary), var(--ui-interactive), var(--ui-interactive-brown));
    border-radius: 0 0 var(--border-radius-md) var(--border-radius-md);
    opacity: 0.6;
    transition: var(--transition-all);
}

.header-container:hover .header-accent {
    opacity: 1;
    width: 80px;
}

/* Scroll effect */
.header-container.scrolled {
    padding: var(--space-md) var(--space-2xl);
    background: linear-gradient(135deg, var(--window-color1) 0%, var(--main-background) 100%);
    backdrop-filter: blur(25px) saturate(200%);
    box-shadow: 0 2px 30px rgba(var(--brand-primary-rgb), 0.12);
}

/* Responsive design */
@media (max-width: 768px) {
    .header-container {
        padding: var(--space-md) var(--space-lg);
    }
    
    .header-content {
        gap: var(--space-sm);
    }
    
    .brand-icon {
        width: 38px;
        height: 38px;
    }
    
    .brand-icon::before {
        font-size: var(--font-size-md);
    }
    
    .header-title {
        font-size: var(--font-size-xl);
    }
    
    .header-tagline {
        font-size: var(--font-size-xs);
    }
    
    .header-accent {
        width: 45px;
    }
}

@media (max-width: 480px) {
    .header-container {
        padding: var(--space-sm) var(--space-md);
    }
    
    .header-brand {
        gap: var(--space-sm);
    }
    
    .brand-icon {
        width: 32px;
        height: 32px;
    }
    
    .brand-icon::before {
        font-size: var(--font-size-sm);
    }
    
    .header-title {
        font-size: var(--font-size-lg);
    }
    
    .header-tagline {
        display: none;
    }
    
    .header-accent {
        width: 35px;
        height: 2px;
    }
}

/* Animation keyframes */
@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.brand-icon:hover .icon-gradient {
    animation: shimmer 0.6s ease-out;
}
</style>
