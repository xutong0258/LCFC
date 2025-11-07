import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue')
  },
  {
    path: '/detail',
    name: 'detail',
    component: () => import('@/views/dataView/detail.vue'),
    props: (route) => ({ id: route.query.id })
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
