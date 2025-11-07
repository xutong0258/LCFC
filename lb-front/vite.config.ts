import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: {
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          // 将 Vue 相关库分离到单独的 chunk
          vue: ['vue', 'vue-router', 'pinia'],
          // 将 Element Plus 分离到单独的 chunk
          'element-plus': ['element-plus', '@element-plus/icons-vue'],
          // 将工具库分离到单独的 chunk
          utils: ['axios']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api/': {
        target: 'http://8.133.193.93:8080',
        changeOrigin: false,
        ws: true,
      },
    },
  },
});
