<template>
    <div class="register-container">
      <form @submit.prevent="register">
        <h2>注册</h2>
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="user.username" required />
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input type="email" id="email" v-model="user.email" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="user.password" required />
        </div>
        <div class="form-group">
          <label for="confirm-password">确认密码</label>
          <input type="password" id="confirm-password" v-model="confirmPassword" required />
        </div>
        <div class="button-container">
  			<button @click="goToMain">登录</button>
			  <button @click="goToRegister">注册</button>
		</div>
      </form>
    </div>
  </template>
  
  <script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const router = useRouter();
const user = ref({
  username: '',
  email: '',
  password: '',
});

const confirmPassword = ref('');

const goToMain = () => {
  router.push('/');
};

const goToRegister = async () => {
  if (user.value.password !== confirmPassword.value) {
    ElMessage.error('密码不匹配');
    return;
  }
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/register', {
      username: user.value.username,
      email: user.value.email,
      password: user.value.password,
    });
    console.log('注册响应：', response.data);
    if (response.data.status === 'success') {
      ElMessage.success('注册成功');
      router.push('/'); // 可能需要跳转到登录页面或其他页面
    } else {
      ElMessage.error('注册失败：' + response.data.message);
    }
  } catch (error) {
    console.error('注册失败：', error);
    ElMessage.error('注册失败，请稍后再试');
  }
};
</script>
  
  <style scoped>
  .button-container {
	display: grid;
	grid-template-columns: 1fr 1fr; /* 创建两列 */
	gap: 10px; /* 设置按钮之间的间隔 */
  }
  
  .button-container button {
	width: 100%; /* 使按钮宽度填满其所在的列 */
  }
  
  .register-container {
    max-width: 300px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"],
  input[type="email"],
  input[type="password"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>