<template>

  <h2>视频播放</h2>

  <div class="common-layout">
    <el-container>
      <el-main>
        <div aria-label="余天王视频播放器">
          <video width="800" height="300" controls>
            <source
                src="https://cloud.video.taobao.com/vod/play/czROWko4MjFLZ2R3cDAxOHc5c2hNeFpkQXVLbw/dDdzUUx3SkEyZUs4c0s2UGVsNUp6SlVVQk5YeDlRTjdFeVFFTFA3bmNUSWpPNlRNbHV3R04zTmh3PT0"
                type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
      </el-main>
      <el-aside width="200px">
        <div>选择视频</div>
        <el-scrollbar height="400px">
          <p v-for="item in items" :key="item" class="scrollbar-demo-item">{{ item.title }}</p>
        </el-scrollbar>
      </el-aside>

    </el-container>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue";
import _axios from "@/plugins/axios.js";
import {userInfoStore} from "@/stores/counter.js";

const items = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
const store = userInfoStore()
onMounted(function (e) {
  console.log("获取视频列表")
  _axios.get("/api/video/list/", {headers: {token: store.token}}).then(function (res) {
    if (res.data.code === 0) {
      items.value = res.data.data
    } else {
      console.log("请求异常", res)
    }
  }).catch(function (errors) {
    console.log(errors)
  })

  _axios.get("/pi/video/blog/").then(function (res) {
    if (res.data.code === 0) {
      items.value = res.data.data
    } else {
      console.log("请求异常", res)
    }
  }).catch(function (errors) {
    console.log(errors)
  })
})

</script>

<style scoped>
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
.scrollbar-demo-item:hover {
  /* 添加鼠标悬浮的样式 */
  cursor: pointer;
  /* 鼠标悬浮时的背景色 */
  background-color: #f0f0f0;
}
</style>