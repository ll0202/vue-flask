//引入createapp用于创建
import { createApp } from 'vue'
//引入app根组件
import App from './App.vue'
//引入路由
import router from './router'
// import axios from 'axios'

// Vue.prototype.$axios = axios


const app =createApp(App)
app.use(router)
app.mount('#app')

