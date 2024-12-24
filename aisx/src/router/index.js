// 创建路由器
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(), // 使用HTML5模式
  routes: [
    {
      path: '/',
      redirect: '/login' // 默认重定向到 login 页面
    },
    {
      path: '/login',
      component: () => import('@/components/login/Login.vue') // 登录页面
    },
    {
      path: '/register',
      component: () => import('@/components/login/register.vue') // 注册页面
    },
    {
      path: '/main',
      component: () => import('@/components/layouts/MainNav.vue'), // 导航栏会始终显示
      children: [
        {
          path: '', // 默认子路由，跳转到 /main/menu1
          redirect: '/main/menu1'
        },
        {
          path: 'menu1',
          component: () => import('@/components/views/Menu1/Menu1.vue')
        },
        {
          path: 'menu2',
          component: () => import('@/components/views/Menu2/Menu2.vue')
        },
        {
            path: 'profile',
            component: () => import('@/components/views/Profile/Profile.vue') // 编辑个人信息页面
        },
        {
          path: 'key',
          component: () =>import('@/components/views/key/key.vue')
        }
      ]
    }
  ]
});



router.beforeEach((to, _from, next) => {
  let username = localStorage.getItem('username');
  
  // 如果用户已登录，或者是访问登录页面，则继续
  if (username || to.path === '/login') {
    next();
  } else {
    // 如果用户未登录并且访问的是其他页面，则重定向到登录页面
    next('/login');
  }
});
export default router;
