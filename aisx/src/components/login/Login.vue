<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <h2>登录</h2>
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" ref="usernameInputRef" id="username" v-model="form.username" required />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" ref="passwordInputRef" id="password" v-model="form.password" required />
      </div>
      <div class="button-container">
        <button type="submit">登录</button>
        <button @click="goToRegister">注册</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { login } from '@/api/user'; // 导入user.js中的login函数
import { useTestStore } from '@/stores'; // 引入 Pinia Store

const form = ref({ username: '', password: '' });
const router = useRouter();
const usernameInputRef = ref(null);
const passwordInputRef = ref(null);

// 使用 Pinia Store
const testStore = useTestStore();


// 登录操作
const handleLogin = async () => {
  if (!form.value.username) {
    ElMessage.error("用户名不能为空");
    usernameInputRef.value.focus();
    return;
  }
  if (!form.value.password) {
    ElMessage.error("密码不能为空");
    passwordInputRef.value.focus();
    return;
  }

  try {
    const res = await login(form.value.username, form.value.password);

    const data = res.data;
    console.log(res.data)
    if (data.status === 1) {
      ElMessage.success(`尊敬的${form.value.username},您已登录成功`);

      // 保存 token 和用户信息
      // localStorage.setItem('token', data.token);
      localStorage.setItem('username', data.username);
      if (data.photo) {
        testStore.setUserInfo(data.username, data.photo ? `data:image/png;base64,${data.photo}` : '');
        // localStorage.setItem('photo', `data:image/png;base64,${data.photo}`); // 保存头像
      }

      // 跳转到主界面
      router.push('/main'); 
      form.value = { username: '', password: '' }; // 清空表单
    } else if (data.status === 2) {
      ElMessage.error("密码错误！");
      passwordInputRef.value.focus();
    } else if (data.status === 3) {
      ElMessage.error("该用户名暂未注册,请先注册吧");
      form.value = { username: '', password: '' };
    } else {
      ElMessage.error("登录失败，请稍后再试");
    }
  } catch (error) {
    console.error(error);
    ElMessage.error("登录失败，请稍后再试");
  }
};


// 跳转到注册页面
const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }

.button-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.button-container button {
  width: 100%;
}

.login-container {
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
input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}
</style>
