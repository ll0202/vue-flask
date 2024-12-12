//创建路由器
import { createRouter,createWebHashHistory ,createWebHistory} from "vue-router";

//引入每个组件
import Login from '@/components/login/Login.vue'
import Register from '@/components/login/register.vue'

const router = createRouter({
    history:createWebHistory(),//工作模式
    routes:[
        {
            path:'',
            component:()=>import('@/components/login/Login.vue')
        },
        {
            path:'/Register',
            component:()=>import('../components/login/Register.vue')
        },
        {
            path:'/main',
            component:()=>import('../components/main.vue')
        }
        
        
    ]
})
//暴露
export  default router