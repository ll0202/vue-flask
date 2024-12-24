<template>
  <div class="content">
    <!-- 下拉框 -->
    <div class="dropdown">
      <select v-model="selectedKey" class="dropdown-select" @change="handleSelection">
        <option disabled value="">选择模型</option>
        <option v-for="key in chatKeys" :key="key.id" :value="key">
          {{ key.name }}
        </option>
      </select>
    </div>

    <div class="chat-box">
      <!-- 渲染消息 -->
      <div v-for="(message, index) in messages" :key="index" class="chat-message">
        <div
          :class="[
            'message-container',
            message.role === 'assistant' ? 'message-container-assistant' : 'message-container-user'
          ]"
        >
          <!-- 显示角色名称 -->
          <span class="message-role">
            {{ message.role === 'assistant' ? '助手' : '用户' }}
          </span>
          <div
            :class="[
              'message-bubble',
              message.role === 'assistant' ? 'message-bubble-assistant' : 'message-bubble-user'
            ]"
          >
            <p class="message-text">{{ message.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue';
import { chatSelectionKey } from '@/api/user';
import { useTestStore } from '@/stores/index';

// 获取 Pinia store
const testStore = useTestStore();
const selectedKey = ref('');

// 获取模型列表
const chatKeys = computed(() => testStore.chatKeys);

// 获取消息列表
const messages = computed(() => testStore.messages);

// 检查消息数量并存储第一条消息
const checkMessages = () => {
  testStore.storeFirstMessageIfTwoMessages(testStore.messages);
};

// 监听 messages 数组的变化，并在变化时检查消息数量
watchEffect(() => {
  checkMessages();
});

// 选择模型时触发
const handleSelection = async () => {
  if (selectedKey.value) {
    console.log(selectedKey.value.name);
    try {
      const response = await chatSelectionKey(selectedKey.value.name);
      console.log('响应数据:', response.data);
    } catch (error) {
      console.error('请求失败:', error);
    }
  }
};
</script>

  
  <style scoped>
  .content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .chat-box {
    border: 1px solid #ccc;
    padding: 10px;
    max-height: 400px;
    overflow-y: auto;
    /* background-color: #a5db7b; */
    /* background-image: url(); */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 778px;
    height: 390px;
  }
  
  .chat-message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
  }
  
  .message-container {
    display: flex;
    flex-direction: column;
    max-width: 760px;
  }
/*   
  .message-container-assistant {
    align-items: flex-start;
  }
  
  .message-container-user {
    align-items: flex-end;
  } */
  
  .message-role {
    font-size: 12px;
    color: #666;
    margin-bottom: 5px;
  }
  
  .message-bubble {
    padding: 10px;
    border-radius: 10px;
    word-wrap: break-word;
  }
  
  .message-bubble-assistant {
    background-color: #e0e0e0;
    align-self: flex-start;
  }
  
  .message-bubble-user {
    background-color: #d1e7dd;
    align-self: flex-end;
  }
  
  .message-text {
    margin: 0;
  }
  
  .dropdown {
    position: absolute;
    top: 20px;
    left: 55%;
    margin-bottom: 20px;
    padding-top: 10px;
  }
  
  .dropdown-select {
    padding: 5px;
    font-size: 14px;
  }
  </style>
  