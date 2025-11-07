<template>
  <div class="about">
    <el-container>
      <el-header>
        <el-page-header @back="goBack" content="关于页面">
          <template #icon>
            <el-icon><ArrowLeft /></el-icon>
          </template>
        </el-page-header>
      </el-header>
      
      <el-main>
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>项目信息</span>
            </div>
          </template>
          
          <el-descriptions :column="1" border>
            <el-descriptions-item label="项目名称">LB Front</el-descriptions-item>
            <el-descriptions-item label="版本">1.0.0</el-descriptions-item>
            <el-descriptions-item label="框架">Vue 3 + TypeScript</el-descriptions-item>
            <el-descriptions-item label="UI库">Element Plus</el-descriptions-item>
            <el-descriptions-item label="状态管理">Pinia</el-descriptions-item>
            <el-descriptions-item label="路由">Vue Router</el-descriptions-item>
            <el-descriptions-item label="构建工具">Vite</el-descriptions-item>
          </el-descriptions>
          
          <div style="margin-top: 20px; text-align: center;">
            <el-alert
              title="项目已成功初始化！"
              type="success"
              :closable="false"
              show-icon>
            </el-alert>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.about {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>