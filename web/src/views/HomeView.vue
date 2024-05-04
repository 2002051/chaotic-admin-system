  <template>


    <div class="common-layout">
      <el-container>
        <el-header style="height: 60px;background-color: #ffffff;padding: 0 50px">
          <div class="head_nav">
            <div>
              <!--             左边-->
              <h2><el-image style="width: 120px;height: 50px" :src="static_url + '/media/config/logo.jpg'"/></h2>
            </div>

            <div>
              <!--              右边-->

              <el-dropdown>

                   <span class="el-dropdown-link" style="height: 30px;font-size: 15px;">
                    欢迎：{{ store.nickname ? store.nickname : "余天王万岁(找不到用户名)" }}

                    <el-icon class="el-icon--right">
                      <arrow-down/>
                    </el-icon>
                        <el-avatar
                            :src="store.userDict.avatar?static_url + store.userDict.avatar:'/media/avatar_img/default.jpg'"
                            style="padding-left: 5px"
                        />
                  </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item>用户信息</el-dropdown-item>
                    <el-dropdown-item divided @click="doLogout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>

        </el-header>

        <el-container class="main">
          <!--        左侧导航-->
          <el-aside width="200px" style="background-color: grey">

            <el-menu :router="true" :default-active="route.name" background-color="#001529" text-color="#ffffff">


              <el-menu-item index="overview">
                <el-icon>
                  <icon-menu/>
                </el-icon>
                <span>数据总览</span>
              </el-menu-item>
              <el-menu-item index="book">
                <el-icon>
                  <Notebook/>
                </el-icon>
                <span>书籍管理</span>
              </el-menu-item>
              <el-menu-item index="campus">
                <el-icon>
                  <School/>
                </el-icon>
                <span>校区管理</span>
              </el-menu-item>
              <el-sub-menu index="user1" >
                <template #title>
                  <el-icon>
                    <User/>
                  </el-icon>
                  <span>人员管理</span>
                </template>
                <el-menu-item index="user" :route='{name:"student"}'>学生管理</el-menu-item>
                <el-menu-item index="biographical" :route='{name:"biographical"}'>简历列表</el-menu-item>
                <el-menu-item index="media" :route='{name:"media"}'>媒体管理</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
              </el-sub-menu>

              <el-menu-item index="video">
                <el-icon>
                  <VideoPlay/>
                </el-icon>
                <span>视频播放</span>
              </el-menu-item>
              <!--       二级菜单     -->
              <el-sub-menu index="user2" disabled>
                <template #title>
                  <el-icon>
                    <User/>
                  </el-icon>
                  <span>会员中心</span>
                </template>
                <el-menu-item index="vip" :route='{name:"##"}'>测试管理</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
              </el-sub-menu>
              <el-sub-menu index="user3" disabled>
                <template #title>
                  <el-icon>
                    <User/>
                  </el-icon>
                  <span>会员中心</span>
                </template>
                <el-menu-item index="vip" :route='{name:"##"}'>测试管理</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
              </el-sub-menu>
              <el-sub-menu index="user4" disabled>
                <template #title>
                  <el-icon>
                    <User/>
                  </el-icon>
                  <span>会员中心</span>
                </template>
                <el-menu-item index="vip" :route='{name:"##"}'>测试管理</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
              </el-sub-menu>
              <el-sub-menu index="user5" disabled>
                <template #title>
                  <el-icon>
                    <User/>
                  </el-icon>
                  <span>会员中心</span>
                </template>
                <el-menu-item index="vip" :route='{name:"##"}'>测试管理</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
                <el-menu-item index="##" :route='{name:"##"}'>测试目录</el-menu-item>
              </el-sub-menu>
            </el-menu>
          </el-aside>
          <!--        核心功能-->
          <el-main style="background-color: #f0f2f5;padding: 20px">
            <el-card style="max-width: 100%;width: 100%">

              <router-view/>

            </el-card>
          </el-main>
        </el-container>
      </el-container>
    </div>


  </template>

  <script setup>
  import {Document, Menu as IconMenu, Location, Setting, Notebook,School,User,VideoPlay} from '@element-plus/icons-vue'
  import {ref, onBeforeMount, onMounted} from 'vue'
  import {useCookies} from "vue3-cookies";
  import {userInfoStore} from "@/stores/counter.js";
  import {useRoute, useRouter} from 'vue-router'
  import {static_url} from "@/plugins/config.js";
  const src = ref("../assets/logo.jpg")


  const activeIndex = ref('')
  const handleSelect = (key, keyPath) => {
    console.log(key, keyPath)
  }
  const handleOpen = (key, keyPath) => {
    console.log(key, keyPath)
  }
  const handleClose = (key, keyPath) => {
    console.log(key, keyPath)
  }
  const store = userInfoStore();
  const {cookies} = useCookies() // 导入vue3使用cookies
  // const token = cookies.get("token")
  const router = useRouter()
  const route = useRoute()


  function doLogout(e) {

    store.Logout()
    console.log("注销")
    router.push({name: "login"})
  }


  </script>


  <style scoped>


  body {
    margin: 0px;
  }

  .flex-grow {
    flex-grow: 1;
  }

  body {
    margin: 0;
    border-radius: 20px;
  }

  .head_nav {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .el-dropdown-link {
    cursor: pointer;
    display: flex;
    align-items: center;
    margin: auto;
  }

  .main {
    /*100vh表示可见窗口的百分之一百*/
    height: calc(100vh - 50px);
  }

  .white > * {
    color: white;
  }
  </style>