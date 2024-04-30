import axios from 'axios';
// import {userInfoStore} from "@/stores/counter.js";
import {useRouter} from "vue-router";
import {static_url} from "@/plugins/config.js";

let config = {
    baseURL: static_url,   // 默认的路由前缀
    timeout: 2000,  // 请求超市时间，单位(毫秒)
    headers: {
        'Content-Type': 'application/json',

    }
}

const _axios = axios.create(config)
const router = useRouter()

// axio拦截器  即请求拦截器

_axios.interceptors.request.use(function (config) {



    return config;
})

_axios.interceptors.response.use(function (response) {
    // console.log("来自响应拦截器", response)
    if (response.data.code === "1003") {
        router.replace({name: "login"})
    }
    return response
}, function (error) {
// 此方法类似.then  当你响应的状态码不是401 那么会走这断逻辑
    console.log("拦截器异常 ", error)
    return error

})

export default _axios;  // 到处已经添加过初始内容的axios类