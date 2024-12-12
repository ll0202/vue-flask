import service from './index.js'
//密码登录
export function Register (data) {
  return service.request({
    method: "post",
    url: "/register/",
    // data: createObj(data).fd
    data: data
  });
}
export function Login (data) {
  return service.request({
    method: "post", // 后端对应的请求方式
    url: "/login/", //对应后端路由地址在uris文件中
    // data: createObj(data).fd
    data: data
  });
}
export function Get_information(data){
  return service.request({
    method:"post",
    url:"/getuser/",
    data:data
  });
}
export function Translate(data){
  return service.request({
    method:"post",
    url:"/translate/",
    data: data
  });
}
export function UpdatePassword(data){
  return service.request({
    method: "post",
    url: "/change/",
    data: data
  });
}
export function GetDepartmentAll(data){
  return service.request({
    method:"post",
    url:"/get_all/",
    data:data
  })
}
export function SubUserList(data){
  return service.request({
    method:"post",
    url:"/SubUserList/",
    data:data
  })
}
export function SubDepart(data){
  return service.request({
    method:"post",
    url:"/SubDepart/",
    data:data
  })
}
export function UpdateDepart(data){
  return service.request({
    method:"post",
    url:"/UpdateDepart/",
    data:data
  })
}
export function AddDepart(data){
  return service.request({
    method:"post",
    url:"/AddDepart/",
    data:data
  })
}
export function addUser(data){
  return service.request({
    method:"post",
    url:"/addUser/",
    data:data
  })
}
export function Add_manager(data){
  return service.request({
    method:"post",
    url:"/Add_manager/",
    data:data
  })
}
export function Deletemanager(data){
  return service.request({
    method:"post",
    url:"/Delete_manager/",
    data:data
  })
}
export function GetUser(data){
  return service.request({
    method:"post",
    url:"/GetUser/",
    data:data
  })
}
export function DeleteMember(data){
  return service.request({
    method:"post",
    url:"/DeleteMember/",
    data:data
  })
}
export function Temp(data){
  return service.request({
    method: "post",
    url: "/temp/",
    data: data
  });
}

export function Logout (data) {
  return service.request({
    method: "post",
    url: "/org/logout",
    // data: createObj(data).fd
    data: data
  });
}
export function getUser (data) {
  return service.request({
    method: "post",
    url: "/org/getuser",
    // data: createObj(data).fd
    data: data
  });
}

export function editUser (data) {
  return service.request({
    method: "post",
    url: "/org/edituser",
    // data: createObj(data).fd
    data: data
  });
}
export function editPassword (data) {
  return service.request({
    method: "post",
    url: "/org/editpassword",
    // data: createObj(data).fd
    data: data
  });
}
export function getUserByToken (data) {
  return service.request({
    method: "post",
    url: "/org/signin",
    // data: createObj(data).fd
    data: data
  });
}

export function refreshByToken (data) {
  return service.request({
    method: "post",
    url: "/org/refreshtoken",
    // data: createObj(data).fd
    data: data
  });
}

