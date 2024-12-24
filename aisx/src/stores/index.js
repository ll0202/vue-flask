// stores/index.js
import { defineStore } from 'pinia';

export const useTestStore = defineStore('Test', {
  state: () => {
    return {
      // 添加头像和用户名
      userAvatar: '',  // 用户头像
      userUsername: '',  // 用户名
      chatKeys: [],  // 用于存储 chat_key 列表
      imageKeys: [], // 用于存储 image_key 列表
      news: [], // 新增状态，用于存储所有符合条件的第一条消息
      messages: [] // 用于存储消息列表
    };
  },
  persist: true,  // 启用持久化，确保数据会被保存在本地
  getters: {},
  actions: {
    // 添加消息到 messages 数组
    addMessage(message) {
      this.messages.push(message);
    },
    // 添加key
    addKey(type, keyData) {
      // 根据传入的 type 判断将 key 添加到哪个列表
      if (type === 'chat') {
        this.chatKeys.push(keyData);  // 将 chat key 添加到 chatKeys 数组
      } else if (type === 'image') {
        this.imageKeys.push(keyData);  // 将 image key 添加到 imageKeys 数组
      }
    },

    // 设置用户名和头像
    setUserInfo(username, avatar) {
      this.userUsername = username;
      this.userAvatar = avatar;
    },

    // 重置所有的 keys
    resetKeys() {
      this.chatKeys = [];
      this.imageKeys = [];
    },
    // 新增操作，用于存储第一条消息
    storeFirstMessageIfTwoMessages(messages) {
      if (messages.length === 2) {
        this.news.push(messages[0]); // 将第一条消息添加到 news 数组
      }
    },
  },
});
