<template>
    <div class="input-container">
      <textarea 
        class="large-input" 
        v-model="inputValue" 
        placeholder="请输入内容" 
        @keydown.enter.prevent="sendData"
        @keydown.ctrl.enter="addNewLine"
      ></textarea>
      <button class="send-button" @click="sendData">发送</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { ElMessage } from 'element-plus';
  import { SendMessage } from '@/api/user';
  
  const inputValue = ref('');
  const emit = defineEmits(['sendMessage', 'updateModelData']);
  
  // 发送数据
  const sendData = async () => {
    if (!inputValue.value) {
      ElMessage.error('请输入内容后再发送');
      return;
    }
  
    try {
      const response = await SendMessage(inputValue.value);
      console.log(response.data); // 输出返回数据
  
      if (response.data.status === 1) {
        ElMessage.success('发送成功');
        const userMessage = inputValue.value;
        const modelAnswer = response.data.response;
        console.log('userMessage', userMessage);
        console.log('modelAnswer', modelAnswer);
        // 触发事件，将 response.data 传递给父组件
        emit('sendMessage', { userMessage, modelAnswer });
        inputValue.value = '';
      } else {
        ElMessage.error("发送失败");
      }
    } catch (error) {
      console.error(error);
      ElMessage.error("发送失败，请稍后再试");
    }
  };
  
  // 为了支持Ctrl + Enter换行
  const addNewLine = (event) => {
    if (event.ctrlKey && event.key === 'Enter') {
      inputValue.value += '\n'; // 添加新的一行
    }
  };
  </script>
  
  <style scoped>
  .input-container {
    position: relative;
    width: 780px;
  }
  
  .large-input {
    width: 799px;
    height: 150px;
    font-size: 15px;
    padding: 10px;
    box-sizing: border-box; /* 确保padding和边框不影响宽度 */
    resize: none; /* 禁用文本框调整大小 */
    text-align: left;
    text-indent: 0;
    overflow-y: auto; /* 允许滚动 */
  }
  
  .send-button {
    position: absolute;
    right: 10px;
    bottom: 10px;
    background-color: #409EFF;
    color: white;
    padding: 8px 16px;
    font-size: 14px;
    border: none;
    cursor: pointer;
  }
  
  .send-button:hover {
    background-color: #66b1ff;
  }
  </style>
  