import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MainRecView from '../views/MainRecView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/how-it-works',
      name: 'how-it-works',
      component: () => import('../views/HowItWorksView.vue')
    },
    {
      path: '/begin',
      name: 'begin',
      component: () => import('../views/BeginView.vue')
    },
    {
      path: '/type',
      name: 'type',
      component: () => import('../views/TypeSelectView.vue')
    },
    {
      path: '/color',
      name: 'color',
      component: () => import('../views/ColorSelect.vue')
    },
    {
      path: '/appearance',
      name: 'appearance',
      component: () => import('../views/AppearanceSelect.vue')
    },
    {
      path: '/item',
      name: 'item',
      component: () => import('../views/ItemSelectView.vue')
    },
    {
      path: '/rec-board',
      name: 'rec-board',
      component: MainRecView
    }
  ]
})

export default router 