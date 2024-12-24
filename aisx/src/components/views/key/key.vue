<template>
  <div class="app">
    <div class="left_container">
      <div class="input-group">
      <label for="chat_key">chat_key</label>
      <button type="button" class="in_key" @click="showModal('chat')">添加</button>
      </div>
        <!-- 显示 chat_key 列表 -->
      <div class="key-list">
        <h3>Chat Keys</h3>
        <ul>
          <li v-for="(key, index) in testStore.chatKeys" :key="index">
            <!-- {{ index }}: {{ key.name }} -->
            {{ key.name }}
            <button @click="deleteKeyByIndex(index, 'chat')">删除</button>
            <button>编辑</button>
          </li>
        </ul>
      </div>   
    </div>
    
    <div class="right_container">
      <!-- image key 添加按钮 -->
      <div class="input-group">
        <label for="image_key">image_key</label>
        <button type="button" class="in_key" @click="showModal('image')">添加</button>
      </div>

      <!-- 显示 image_key 列表 -->
      <div class="key-list">
        <h3>Image Keys</h3>
        <ul>
          <li v-for="(key, index) in testStore.imageKeys" :key="index">
            <!-- {{ index }}: {{ key.name }} -->
            {{ key.name }}
            <button @click="deleteKeyByIndex(index, 'image')">删除</button>
            <button>编辑</button>
          </li>
        </ul>
      </div>

    </div>
  

    <!-- 弹出表单 (悬浮框) -->
    <div v-if="isModalVisible" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>添加key</h3>
        <form>
          <label for="platform">* Platform</label>
          <input type="text" id="platform" placeholder="请输入Platform" v-model="formData.platform" />

          <label for="name">* Name</label>
          <input type="text" id="name" placeholder="请输入Name" v-model="formData.name" />

          <label for="url">* URL</label>
          <input type="text" id="url" placeholder="请输入URL" v-model="formData.url" />

          <label for="val">* Val</label>
          <input type="text" id="val" placeholder="请输入Value" v-model="formData.val" />

          <!-- 按钮 -->
          <div class="button-group">
            <button type="button" @click="closeModal">关闭</button>
            <button type="submit" @click.prevent="saveForm">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { saveKey, deleteKey as deleteKeyAPI } from '@/api/user';  // 引入 API
import { useTestStore } from '@/stores';  // 引入 Pinia Store

const isModalVisible = ref(false);
const formData = ref({
  platform: '',
  name: '',
  url: '',
  val: '',
});
const testStore = useTestStore();  // 使用 Pinia Store
const currentKeyType = ref('');  // 用于存储当前的 key 类型

// 显示弹出框时传递 keyType
const showModal = (keyType) => {
  isModalVisible.value = true;
  currentKeyType.value = keyType;  // 记录当前选择的 key 类型
  console.log(`正在添加: ${keyType}`);
};

// 关闭弹出框
const closeModal = () => {
  isModalVisible.value = false;
};

// 重置表单
const resetForm = () => {
  formData.value = {
    platform: '',
    name: '',
    url: '',
    val: '',
  };
};

// 保存表单数据并传递到后端
const saveForm = async () => {
  try {
    const username = localStorage.getItem('username');
    if (!username) {
      ElMessage.error('用户未登录或ID不可用');
      return;
    }

    // 发送 POST 请求将数据传递给后端
    const keyData = {
      platform: formData.value.platform,
      name: formData.value.name,
      url: formData.value.url,
      val: formData.value.val,
      type: currentKeyType.value,  // 传递 key 类型
    };
    console.log("keydata:", keyData);

    const response = await saveKey(
      keyData.platform,
      keyData.name,
      keyData.url,
      keyData.val,
      username,
      keyData.type
    );

    console.log('后端响应:', response.data);
    ElMessage.success('保存成功！');

    // 将 key 数据保存到 Pinia
    testStore.addKey(currentKeyType.value, keyData);  // 根据类型将 key 保存到对应的列表

    // 清空表单数据
    resetForm();

    // 关闭弹出框
    closeModal();
  } catch (error) {
    console.error('保存失败:', error);
    ElMessage.error('保存失败，请重试！');
  }
};

// 删除 key 根据索引
const deleteKeyByIndex = async (index, type) => {
  try {
    const key = testStore[type + 'Keys'][index];
    if (!key) {
      ElMessage.error('Key不存在');
      return;
    }

    const username = localStorage.getItem('username');
    if (!username) {
      ElMessage.error('用户未登录或ID不可用');
      return;
    }
    // 先删除数据库中的 key
    const response = await deleteKeyAPI(key.name, username, type);  // 使用 key 的 name 和 type 删除数据库中的 key

    if (response.data.status === 1) {
      // 数据库删除成功后，更新 Pinia 状态
      testStore[type + 'Keys'].splice(index, 1);  // 通过索引删除 Pinia 中的 key
      ElMessage.success('删除成功！');
    } else {
      ElMessage.error('数据库删除失败，请重试！');
    }
  } catch (error) {
    console.error('删除失败:', error);
    ElMessage.error('删除失败，请重试！');
  }
};

</script>


<style>
.app {
  display: flex;
  justify-content: space-around;
  padding: 20px;
}

.input-group {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.left_container {
  display: flex;
  flex-direction: column;
}
.right_container{
  display: flex;
  flex-direction: column;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

form {
  display: flex;
  flex-direction: column;
}

form label {
  margin-top: 10px;
}

form input {
  padding: 5px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.button-group {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
 
button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #f0f0f0;
}

.key-list {
  margin-top: 20px;
}

.key-list ul {
  list-style-type: none;
  padding: 0;
}

.key-list li {
  margin: 5px 0;
}
</style>
