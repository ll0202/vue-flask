<template>
  <div class="container">
    <!-- 接收 Mylist 子组件传来的 Base64 图像数据 -->
    <Mylist @imageGenerated="handleImageGenerated" />

    <!-- 将 Base64 图像数据通过 props 传递给 Mycontent 子组件 -->
    <Mycontent :imageBase64="imageBase64" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Mylist from "../Menu2/components/Mylist.vue";
import Mycontent from "../Menu2/components/Mycontent.vue";

// 用来存储接收到的 Base64 图像数据
const imageBase64 = ref('');

// 处理从 Mylist 组件传来的 imageGenerated 事件
const handleImageGenerated = (base64Image) => {
  console.log('Received imageBase64 from Mylist:', base64Image); 
  imageBase64.value = base64Image;  // 存储接收到的 Base64 数据
};
</script>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: stretch;
}

.Mylist, .Mycontent {
  flex: 1;
  min-width: 200px;
  margin-right: 10px;
}
</style>
