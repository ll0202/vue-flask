<template>
  <div class="profile-container">
    <h2>个人信息</h2>
    
    <!-- 头像修改部分 -->
    <div class="avatar-preview" @click="$refs.avatarInput.click()">
      <img v-if="avatarPreview" :src="avatarPreview" alt="头像预览" class="avatar-img" />
      <div v-else class="placeholder">点击上传头像</div>
      <input type="file" id="avatar" ref="avatarInput" @change="handleAvatarChange" style="display: none;" />
    </div>
    <!-- 用户信息修改部分 -->
    <form>
      <div class="form-group">
        <label for="account">账号:</label>
        <input type="text" id="account" v-model="account" readonly/>
      </div>
  
      <div class="form-group">
        <label for="username">姓名:</label>
        <input type="text" id="username" v-model="name" />
      </div>
  
      <div class="form-group">
        <label for="email">邮件:</label>
        <input type="email" id="email" v-model="email" />
      </div>
  
      <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" />
      </div>
  
      <div class="button-container">
        <button type="button" class="find-btn" @click="fetchProfile">查询信息</button>
        <button type="button" class="save-btn" @click="updateProfile">修改信息</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { findProfile, saveProfile } from '@/api/user.js'; // 导入user.js中的函数
import { useTestStore } from '@/stores'; // 引入 Pinia Store

const account = ref('');
const name = ref('');
const email = ref('');
const password = ref('');
const avatarPreview = ref(null);
const avatarPath = ref(null);
const testStore = useTestStore();

const getUsername = () => {
  return localStorage.getItem('username') || '';
};

const handleAvatarChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      avatarPreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
    avatarPath.value = file;
  }
};

const fetchProfile = async () => {
  const username = getUsername();
  if (!username) {
    ElMessage.error('用户未登录或ID不可用');
    return;
  }

  try {
    const res = await findProfile(username);
    const user = res.data;
    account.value = user.id;
    name.value = user.username;
    email.value = user.email;
    password.value = user.password;
    if (user.photo) {
      avatarPreview.value = `data:image/jpeg;base64,${user.photo}`;
    } else {
      avatarPreview.value = null;
    }
  } catch (error) {
    console.error('Error fetching profile:', error.response ? error.response.data : error);
    ElMessage.error('查询失败，请检查控制台');
  }
};

const updateProfile = async () => {
  const userid = account.value;
  if (!userid) {
    ElMessage.error('用户未登录或ID不可用');
    return;
  }

  const formData = new FormData();
  formData.append('userid', userid);
  formData.append('username', name.value);
  formData.append('password', password.value);
  formData.append('email', email.value);
  if (avatarPath.value) {
    formData.append('avatar', avatarPath.value);
  }

  console.log('Sending to server2:', Array.from(formData.entries()));

  try {
    const res = await saveProfile(formData);
    ElMessage.success(res.data.message);
    // 在前端更新头像时，将 base64 编码的头像直接存入 Pinia
    const avatarUrl = avatarPreview.value || ''; // 直接使用前端存储的 base64 数据
    testStore.setUserInfo(res.data.username, avatarUrl); // 存储用户名和头像
  } catch (error) {
    console.error('Error saving profile:', error.response ? error.response.data : error);
    ElMessage.error('保存失败，请检查控制台');
  }
};
</script>


<style scoped>
  
  #account {
    cursor: not-allowed; 
  }
  .profile-container {
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 1000px;
    margin: auto;
  }

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.avatar-section {
  position: relative;
  margin-bottom: 20px;
}

.avatar-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border: 2px solid #ddd;
  border-radius: 4px; /* 保持轻微圆角 */
  cursor: pointer;
  overflow: hidden; /* 确保图片不会超出边界 */
  margin-left: 250px;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ddd;
  font-size: 14px;
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
  margin-left: 350px;
}

label {
  margin: 10px 0 5px;
}

input {
  padding: 8px;
  width: 200px;
  margin-bottom: 30px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.button-container {
  margin-bottom: 5px;
  display: flex;
  gap: 15px;
  justify-content: center;
}

button {
  width: 200px; /* 调整为你想要的宽度 */
  height: 35px;;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  
  transition: background-color 0.3s ease;
}

.find-btn {
  background-color: #007bff;
  color: white;
}

.find-btn:hover {
  background-color: #0056b3;
}

.save-btn {
  background-color: #28a745;
  color: white;
}

.save-btn:hover {
  background-color: #218838;
}

input[readonly] {
  background-color: #f1f1f1;
}
</style>