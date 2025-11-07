import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useMainStore = defineStore('main', () => {
  // 状态
  const count = ref(0)
  const user = ref<any>(null)
  
  // 计算属性
  const doubleCount = computed(() => count.value * 2)
  
  // 动作
  const increment = () => {
    count.value++
  }
  
  const decrement = () => {
    count.value--
  }
  
  const reset = () => {
    count.value = 0
  }
  
  const setUser = (newUser: any) => {
    user.value = newUser
  }
  
  return {
    count,
    user,
    doubleCount,
    increment,
    decrement,
    reset,
    setUser
  }
})