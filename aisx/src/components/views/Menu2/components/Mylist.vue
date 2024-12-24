<template>
    <div class="image-generator">
      <textarea v-model="description" placeholder="描述想要生成的图片"></textarea>
      <div class="aspect-ratios">
        <button 
          v-for="ratio in aspectRatios" 
          :key="ratio.ratio" 
          @click="selectAspectRatio(ratio)"
          class="aspect-ratio-button"
        >
          {{ ratio.ratio }}
        </button>
      </div>
      <div class="dimensions">
        <label>宽度:</label>
        <input type="number" v-model.number="width" @input="updateHeight" />
        <label>高度:</label>
        <input type="number" v-model.number="height" @input="updateWidth" />
      </div>
      <div class="generate-button">
        <button @click="generateImage">立即生成</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from 'vue';
  import { ElMessage } from 'element-plus';
  import { sendImage } from '@/api/user';
  
  const emit = defineEmits(['imageGenerated']);  // 用于向父组件发送事件
  
  const description = ref('');
  const aspectRatios = ref([
    { ratio: '16:9', width: 640, height: 360 },
    { ratio: '4:3', width: 640, height: 480 },
    { ratio: '1:1', width: 640, height: 640 },
    { ratio: '4:3', width: 680, height: 512 },
    { ratio: '3:4', width: 512, height: 680 },
    { ratio: '1:1', width: 768, height: 768 },
    { ratio: '9:16', width: 720, height: 1280 },
    { ratio: '16:9', width: 1280, height: 720 },
    { ratio: '1:1', width: 1024, height: 1024 },
  ]);
  
  const selectedAspectRatio = ref('1:1');
  const width = ref(1024);
  const height = ref(1024);
  
  const selectAspectRatio = (ratio) => {
    selectedAspectRatio.value = ratio.ratio;
    width.value = ratio.width;
    height.value = ratio.height;
  };
  
  const updateHeight = () => {
    if (width.value) {
      const ratio = selectedAspectRatio.value.split(':').map(Number);
      height.value = (width.value / ratio[0]) * ratio[1];
    }
  };
  
  const updateWidth = () => {
    if (height.value) {
      const ratio = selectedAspectRatio.value.split(':').map(Number);
      width.value = (height.value / ratio[1]) * ratio[0];
    }
  };
  
  // 用于存储生成的Base64图片
  const imageBase64 = ref('');
  
  // 生成图像并传递给后端
  const generateImage = async () => {
    try {
      const response = await sendImage(description.value, width.value, height.value);
      console.log(response.data);
      console.log(response.data.status);
  
      if (response.data.status === 1 && response.data.image_base64) {
        ElMessage.success(`图片生成请求已发送`);
  
        // 获取Base64图片数据
        const base64Image = response.data.image_base64;
        console.log('Emitting imageGenerated with base64:', base64Image);  // 打印Base64数据
        // 将Base64数据传递给父组件
        emit('imageGenerated', base64Image);
  
        // 将Base64数据存储在本组件中，供展示用
        imageBase64.value = base64Image;
      } else {
        ElMessage.error("请求失败，请稍后再试！");
      }
    } catch (error) {
      ElMessage.error("请求错误");
    }
  };
  </script>
  
  <style>
  .image-generator {
      display: flex;
      flex-direction: column;
      align-items: center;
      background-color: #f8ecd7;
      margin-left: 1px;
      margin-right: 1px;
      /* padding: 20px; */
      border-radius: 10px;
      width: 300px;
      height: 570px;
  }
  
  textarea {
      width: 250px;
      height:150px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      resize: none;
  }
  
  .aspect-ratios {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      margin-top: 30px;
      gap: 10px;
  }
  
  .aspect-ratio-button {
      padding: 10px;
      background-color: #d6e4f0;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
      width: 75px;
      height: 50px;
      font-size: 14px;
      font-weight: bold;
  }
  
  .aspect-ratio-button:hover {
      background-color: #c0d4ec;
  }
  
  .dimensions {
      display: flex;
      flex-direction: row;
      align-items: center;
      margin-top: 40px;
      gap: 10px;
  }
  
  label {
      font-size: 14px;
      font-weight: bold;
  }
  
  input[type="number"] {
      width: 80px;
      padding: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
  }
  
  .generate-button{
      margin-top: 30px;
      
  }
  .generate-button button {
      padding: 10px 20px;
      background-color: #6bbdff;
      color: #fff;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
      font-weight: bold;
  }
  
  .generate-button button:hover {
      background-color: #5aa4e6;
  }
  </style>
  