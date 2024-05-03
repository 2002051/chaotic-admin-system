import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import VueCookies from "vue3-cookies";
//
// import VideoPlayer from 'vue-video-player/src';
// import 'vue-video-player/src/custom-theme.css'
// import 'video.js/dist/video-js.css'
//

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)  //全局注册element-plus
app.use(VueCookies)

app.mount('#app')
