<template>
    <div id="app" class="main-layout">
      <!-- 左侧导航 -->
      <aside class="sidebar">
        <div class="menu-item">菜单1</div>
        <div class="menu-item">菜单2</div>
        <div class="menu-item">菜单3</div>
      </aside>
  
      <!-- 主体框架 -->
      <main class="content">
        <header class="header">
          <div class="avatar-container" @click="toggleUserInfo">
            <img class="avatar" src="@/assets/avatar.png" alt="头像" />
          </div>
        </header>
  
        <section class="user-info" v-if="showUserInfo">
          <form @submit.prevent="saveUserInfo">
            <label>
              姓名：
              <input v-model="user.name" type="text" placeholder="请输入姓名" />
            </label>
            <label>
              电话：
              <input v-model="user.phone" type="text" placeholder="请输入电话" />
            </label>
            <label>
              密码：
              <input v-model="user.password" type="password" placeholder="请输入密码" />
            </label>
            <button type="submit">保存</button>
          </form>
        </section>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        showUserInfo: false,
        user: {
          name: '',
          phone: '',
          password: ''
        },
        avatarUrl: new URL('@/assets/avatar.png', import.meta.url).href
      };
    },
    methods: {
      toggleUserInfo() {
        this.showUserInfo = !this.showUserInfo;
      },
      saveUserInfo() {
        console.log('用户信息已保存:', this.user);
        alert('信息已保存！');
        this.showUserInfo = false;
      }
    }
  };
  </script>
  
  <style>
  body {
    margin: 0;
    font-family: Arial, sans-serif;
    display: flex;
    height: 100vh;
  }
  
  .main-layout {
    display: flex;
    width: 100%;
  }
  
  .sidebar {
    width: 200px;
    background-color: #f0f0f0;
    padding: 10px;
    display: flex;
    flex-direction: column;
  }
  
  .menu-item {
    padding: 10px;
    margin: 5px 0;
    background-color: #fff;
    cursor: pointer;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  .content {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .header {
    background-color: #00bcd4;
    padding: 10px;
    color: #fff;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }
  
  .avatar-container {
    background-color: #00bcd4;
    width: 90%;
    cursor: pointer;
  }
  
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  
  .user-info {
    margin: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f9f9f9;
  }
  
  label {
    display: block;
    margin-bottom: 10px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    background-color: #00bcd4;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #019aaa;
  }
  </style>
  