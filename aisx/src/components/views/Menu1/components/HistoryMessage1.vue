<template>
  <div class="history">
    <button @click="handleCreateChat">新建聊天</button>
    <div class="content">
      <ul>
        <li v-for="(message, index) in news" :key="message.id" @click.stop="handleMessageClick(message)">
          {{ message.content }}
          <button @click.stop="openEditModal(index, message.content)">修改</button>
          <button @click="deleteMessage(index)">删除</button>
        </li>
      </ul>
    </div>
    <div class="button-group">
      <button @click="clearChat">删除聊天</button>
      <button @click="deleteChat">清空聊天</button>
    </div>
    <!-- 修改弹窗 -->
    <div v-if="isModalOpen" class="modal">
      <div class="modal-content">
        <h3>编辑消息</h3>
        <input v-model="editedMessage" type="text" />
        <div class="modal-buttons">
          <button @click="saveMessage(editIndex)">保存</button>
          <button @click="closeEditModal">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useTestStore } from '@/stores/index';
import { createChat, getMessage, deletechatMessage } from '@/api/user';

// Pinia store
const testStore = useTestStore();
const news = computed(() => testStore.news);

// 弹窗和编辑状态相关变量
const isModalOpen = ref(false);
const editIndex = ref(null);
const editedMessage = ref('');

// 打开编辑弹窗
const openEditModal = (index, content) => {
  editIndex.value = index;
  editedMessage.value = content;
  isModalOpen.value = true;
};

// 关闭编辑弹窗
const closeEditModal = () => {
  isModalOpen.value = false;
  editIndex.value = null;
  editedMessage.value = '';
};

// 保存修改后的消息
const saveMessage = (index) => {
  if (index !== null) {
    testStore.news[index].content = editedMessage.value;
  }
  closeEditModal();
};

// 删除消息
const deleteMessage = async (index) => {
  try {
    const message = testStore.news[index]; // 获取要删除的消息
    const news_ID = message.content.split(' ').pop(); // 获取消息中的 ID
    console.log('点击消息，news_ID:', news_ID);

    // 调用删除消息的 API
    const resp = await deletechatMessage(news_ID);

    console.log(resp.data); // 打印返回的响应数据

    if (resp.data.status === 1) {  // 判断删除是否成功
      deleteChat();
      testStore.news.splice(index, 1);  // 从 store 中删除消息
    } else {
      ElMessage.error("删除消息失败，请稍后再试");
    }
  } catch (error) {
    console.error('删除消息时发生错误:', error);
    ElMessage.error("操作失败，请稍后再试");
  }
};


// 创建聊天
const handleCreateChat = async () => {
  try {
    const username = localStorage.getItem('username');
    const response = await createChat(testStore.messages, testStore.news, username);

    console.log('数据已发送，后端返回:', response.data);
    const news_ID = response.data.status;
    if (testStore.news.length > 0) {
      const lastMessage = testStore.news[testStore.news.length - 1];
      lastMessage.content += ` ${news_ID}`;
    } else {
      console.warn('news 数组为空，没有可以拼接的消息');
    }

    testStore.messages = [];
  } catch (error) {
    console.error('发送数据到后端失败:', error);
  }
};

// 显示历史消息
const handleMessageClick = async (message) => {
  try {
    const news_ID = message.content.split(' ').pop();
    console.log('点击消息，news_ID:', news_ID);

    const response = await getMessage(news_ID);
    testStore.messages = [];
    console.log('从后端获取到消息:', response.data);

    response.data.forEach((msg) => {
      const newMessage = {
        content: msg.message,
        role:  msg.sender,
      };
      testStore.addMessage(newMessage);
    });
  } catch (error) {
    console.error('获取消息失败:', error);
  }
};

// 删除所有聊天
const deleteChat = () => {
  testStore.messages = [];
};

// 清除聊天
const clearChat = () => {
  testStore.news = [];
};
</script>

<style scoped>
.history {
  background-color: rgb(194, 191, 191);
  border-radius: 10px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 530px;
}

.content {
  flex-grow: 1;
  overflow-y: auto;
  max-height: 400px;
  width: 100%;
  padding: 10px;
  background-color: rgb(194, 191, 191);
  border-radius: 8px;
}

.content ul {
  list-style: none;
  padding: 0;
}

.content ul li {
  font-size: 12px; /* 列表字体大小 */
  margin: 5px 0;
}

.button-group {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

button {
  margin: 1px;
  padding: 5px 10px;
  font-size:11px;
  border-radius: 5px;
  border: 1px solid transparent;
  background-color:rgb(194, 191, 191);
  cursor: pointer;
}

button:hover {
  background-color: #555;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  text-align: center;
}

.modal-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}
</style>
