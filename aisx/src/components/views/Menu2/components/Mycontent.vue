<template>
    <div class="content">
      <!-- 如果父组件传递了图像数据，则显示图像 -->
      <div v-if="imageBase64">
        <img :src="'data:image/png;base64,' + imageBase64" alt="Generated Image" class="generated-image" />
      </div>
  
      <!-- 模型选择下拉框 -->
      <div class="dropdown">
        <select 
          v-model="selectedKey" 
          class="dropdown-select" 
          @change="handleSelection"
        >
          <option disabled value="">选择模型</option>
          <option 
            v-for="key in imageKeys" 
            :key="key.id" 
            :value="key"
          >
            {{ key.name }}
          </option>
        </select>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, defineProps, watch } from 'vue';
  import { imageSelectionKey } from '@/api/user';
  import { useTestStore } from '@/stores/index';
  
  // 获取 Pinia store
  const testStore = useTestStore();
  
  // 接收父组件传递的图像Base64数据
  const props = defineProps({
    imageBase64: {
      type: String,
      default: ''
    }
  });

    // 打印传递的 Base64 数据
    watch(() => props.imageBase64, (newValue) => {
    console.log('Received imageBase64:', newValue); // 打印Base64数据
    });
    
  // 当前选中的模型
  const selectedKey = ref('');
  
  // 获取模型列表
  const imageKeys = computed(() => testStore.imageKeys);
  
  // 选择模型时触发的逻辑
  const handleSelection = async () => {
    if (!selectedKey.value) {
      console.warn('未选择模型');
      return;
    }
  
    try {
      console.log('已选择模型:', selectedKey.value.name);
      const response = await imageSelectionKey(selectedKey.value.name);
      console.log('请求响应数据:', response.data);
    } catch (error) {
      console.error('模型选择请求失败:', error);
    }
  };
  </script>
  
  <style scoped>
  .content {
    background-color: #f8ecd7;
    width: 650px;
    height: 530px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .dropdown {
    position: absolute;
    top: 20px;
    left: 65%;
    margin-bottom: 20px;
    padding-top: 10px;
  }
  
  .dropdown-select {
    padding: 5px;
    font-size: 14px;
  }
  
  .generated-image {
    max-width: 100%;
    max-height: 300px;
    margin-top: 20px;
    border-radius: 10px;
  }
  </style>
  