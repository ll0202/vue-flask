//引入createapp用于创建
import { createApp } from 'vue'
//引入app根组件
import App from './App.vue'
//引入路由
import router from './router'
// import axios from 'axios'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// Vue.prototype.$axios = axios

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
const app =createApp(App)
app.use(router)
app.use(pinia)
app.mount('#app')

