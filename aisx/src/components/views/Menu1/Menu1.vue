<template>
  <div class="container">
    <div class="history-message">
      <HistoryMessage />
    </div>
    <div class="right-container">
      <div class="content">
        <!-- 将后端返回的数据作为 prop 传递给 MyContent1 -->
        <MyContent1 :messages="messages" />
      </div>
      <div class="input">
        <!-- 监听子组件发送的数据 -->
        <Input @sendMessage="handleSendMessage" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useTestStore } from '@/stores';  // 导入 Pinia store
import HistoryMessage from '../Menu1/components/HistoryMessage1.vue';
import MyContent1 from '../Menu1/components/MyContent1.vue'; // 引入 MyContent1 组件
import Input from '../Menu1/components/Myinput1.vue'; // 引入 Input 组件

// 定义一个响应式变量来存储消息
const messages = ref([]);
// 获取 Pinia store 实例
const testStore = useTestStore();

// 处理从 MyInput 组件发送来的消息
// 处理从 Input 组件发送来的消息
const handleSendMessage = (data) => {
  console.log('子组件的数据：', data); // 打印子组件发送的数据
  
  // 创建用户消息和助手消息
  const userMessage = {
    role: 'user',
    content: data.userMessage,
  };
  const assistantMessage = {
    role: 'assistant',
    content: data.modelAnswer,
  };
  
  // 将消息添加到 Pinia store 中
  testStore.addMessage(userMessage);
  testStore.addMessage(assistantMessage);
  
  // 更新本地 messages 数组（可以省略，如果不依赖它的话）
  messages.value.push(userMessage, assistantMessage);
};
</script>


<style scoped>
.container {
  display: flex;
  height: 100%;
}

.history-message {
  flex: 1;  /* 占满左侧的空间 */
  margin-right: 9px;
}

.right-container {
  display: flex;
  flex-direction: column; /* 垂直排列 Content 和 Input */
  width: 800px;  /* 设置右侧容器的宽度 */
}

.content {
  /* border: 2px solid rgb(51, 202, 149);   */
  /* padding: 1px; */
  height: 400px;
}
.input {
  /* border: 2px solid rgb(111, 77, 159); */
  padding: 1px;
  height: 200px;
}

</style>
