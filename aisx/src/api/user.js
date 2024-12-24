// user.js
import service from './index.js'; // 确保路径正确

export const register = (username, email, password) => {
  return service.post('/register', {
    username,
    email,
    password
  });
};

// 确保login函数也存在
export const login = (username, password) => {
  return service.post('/login', {
    userName: username,
    passWord: password
  });
};

// 获取用户信息
export const findProfile = (username) => {
  return service.get('/profile/find', {
    params: { username }
  });
};

// 保存用户信息
export const saveProfile = (formData) => {
  return service.post('/profile/save', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export const saveKey = (platform,name,url,val,username,type) => {
  return service.post('/key/save',{
    platform: platform,
    name: name,
    url: url,
    val: val,
    username: username,
    type: type
  })
}

export const deleteKey = (keyname, username, type) => {
  return service.post('/key/delete', {
    keyname: keyname,
    username: username,
    type: type
  })
}

export const chatSelectionKey =(keyname) => {
  return service.post('/chat/keyselect',{
    keyname: keyname
  })
}

export const SendMessage =(message) => {
  return service.post('/chat/sendmessage',{
    message: message
  })
}


// 新增 createChat 方法：发送聊天数据到后端
export const createChat = (messages, news, username) => {
  const payload = {
    messages,
    news,
    username,
  };

  // 将数据以 JSON 格式发送到后端
  return service.post('/chat/save', JSON.stringify(payload), {
    // headers: {
    //   'Content-Type': 'application/json', 
    // },
  });
};

export const getMessage = (news_ID) => {
  return service.get('/chat/messages', {
    params: {news_ID}
  }); // 假设这个是后端提供的 API
};

export const deletechatMessage = (news_ID) => {
  return service.get('/chat/delect/message', {
    params: {news_ID}
  }); // 假设这个是后端提供的 API
};


export const sendImage =(description, width, height) => {
  return service.post('/image/send', {
    description: description,
    width: width,
    height: height
  })
}


export const imageSelectionKey =(keyname) => {
  return service.post('/image/keys',{
    keyname: keyname
  })
}

