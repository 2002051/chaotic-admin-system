import {ref, computed} from 'vue'
import {defineStore} from 'pinia'
import {useCookies} from 'vue3-cookies'

const {cookies} = useCookies() // 导入vue3使用cookies

export const userInfoStore = defineStore('counter', () => {
  const userDict = ref(cookies.get("info"))// 要么得到null 要么直接得到对应对象(字典)
  const nickname = computed(() => userDict.value.nickname)
  const token = ref(cookies.get("token"))
  function doSaveInfo(info) {
    cookies.set("info", JSON.stringify(info), 60 * 60 * 24) // 过期时间一天
    userDict.value = info  // 修改userString以调动计算属性userDict等的更新
  }
  function doSaveToken(t){
    cookies.set("token",t,60 * 60 * 24)
    token.value = t
  }
  function Logout() {
    // 清除用户数据
    userDict.value = ref({})
    cookies.remove("info");
    cookies.remove("token");
  }

  return {userDict, doSaveInfo, nickname, Logout,doSaveToken,token}
})
