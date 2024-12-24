<template>
  <div class="container" @click="handleGlobalClick">
    <!-- 侧边导航栏 -->
    <nav class="sidebar">
      <div class="avatar">
        <!-- 动态显示头像 -->
        <img :src="computedAvatar" alt="Avatar" class="avatar-img" @click="toggleMenu" />
        <!-- 点击头像显示的列表 -->
        <div v-if="showMenu" class="menu-list">
          <ul>
            <li><router-link to="/main/profile" class="menu-list-item">个人信息</router-link></li>
            <li><router-link to="/main/key" class="menu-list-item">key管理</router-link></li>
            <li @click="handleSidebarClick">
              <router-link to="/login" class="menu-list-item">退出登录</router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="menu">
        <router-link to="/main/menu1" class="menu-btn">Chat</router-link>
        <router-link to="/main/menu2" class="menu-btn">Image</router-link>
      </div>
    </nav>

    <!-- 主体内容区域 -->
    <div class="main-content">
      <router-view></router-view> <!-- 渲染子路由的组件 -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useTestStore } from '@/stores'; // 引入 Pinia Store

const showMenu = ref(false); // 定义并初始化 showMenu

const testStore = useTestStore();

// 切换菜单显示
const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

// 处理全局点击事件
const handleGlobalClick = (event) => {
  if (showMenu.value && !event.target.classList.contains('avatar-img')) {
    showMenu.value = false;
  }
};

// 使用 computed 来动态响应 Pinia Store 的头像变化
const computedAvatar = computed(() => {
  return testStore.userAvatar || '@/assets/ugly.png'; // 默认头像路径
});


onMounted(() => {
  // 添加全局点击事件监听器
  document.addEventListener('click', handleGlobalClick);
});

// 在组件卸载前移除事件监听器
onBeforeUnmount(() => {
  document.removeEventListener('click', handleGlobalClick);
});

// 退出登录的方法
const logout = () => {
  // 清空 localStorage 中的 'username'
  localStorage.removeItem('username');
  // 重置 Pinia Store 中的状态（如果有需要）
  // testStore.reset();
  // 跳转到登录页面
  router.push('/login');
};

// 监听侧边导航栏的点击事件，并调用 logout 方法
const handleSidebarClick = (event) => {
  // 检查点击事件是否来自退出登录的链接
  if (event.target.closest('.menu-list-item').getAttribute('to') === '/login') {
    logout();
  }
};
</script>


<style scoped>
/* 主容器 */
.container {
  display: flex;
  height: 100vh;
  width: 1000px; /* 这里应该是100%或者其他值，10px太窄了 */
}

/* 侧边栏 */
.sidebar {
  width: 90px;
  background-color: #b4b2b2;
  /* color: white; */
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.avatar {
  margin-bottom: 20px;
}

.avatar-img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  cursor: pointer; /* 鼠标悬停时显示为可点击 */
}

.menu {
  display: flex;
  flex-direction: column;
  font-style: italic;
  width: 100px;
}

.menu-btn {
  text-align: center;
  padding: 10px;
  margin: 15px 0;
  background-color: #b4b2b2;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.menu-btn:hover {
  background-color: #555;
}

.menu-btn.active {
  background-color: #888;
}

/* 主体内容 */
.main-content {
  flex-grow: 1;
  padding: 20px;
  background-color: #f4f4f4;
}

/* 点击头像显示的列表 */
.menu-list {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  padding: 1px;
  width: 130px;
  list-style: none; 
  margin-top: 1px;
  margin-left: 1px;
  opacity: 0.6;
}

.menu-list-item {
  color: black;
  text-decoration: none;
  padding: 1px 0;
}

.menu-list-item:hover {
  background-color: #f4f4f4;
}
</style>