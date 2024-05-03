<template>
  <div style="font-size: 20px  "><strong>媒体管理</strong></div>
  <div style="margin-top: 10px">
    <el-button type="primary" @click="doCreate">新增</el-button>
    <el-button @click="doDeleteSelected">批量删除</el-button>
    <span style="margin-left: 24px;">
    <el-input v-model="kw" style="width: 240px;margin-left: 12px;" placeholder="请输入关键字"/>
      <el-button type="primary" @click="doSearch">
             <el-icon>
                <Search/>
              </el-icon>
      </el-button>
  </span>

    <el-button v-if="!!selectedList.length" :icon="Printer" @click="exportSelectedSub" style="margin-left: 10px;background-color: #eaeaea">导出</el-button>

  </div>

  <div v-loading="loading">
    <el-table  :data="datalist" style="width: 100%;height: 95%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <!--      <el-table-column type="index" label="" :index="indexMethod" />-->
      <el-table-column prop="id" label="ID" width="80"/>
      <el-table-column prop="title" label="名称" width="180"/>
      <el-table-column prop="image" label="图片展示" min-width="80">
        <template #default="scrop">
          <el-image style="width: 100px; height: 100px" :src="static_url + scrop.row.image"/>
        </template>
      </el-table-column>
      <!--      <el-table-column prop="campus" label="校区" width="180"/>-->
      <el-table-column prop="audio" label="音频展示" min-width="80">
        <template #default="scrop">
          <el-link target="_blank" type="success" :href="!!scrop.row.audio?static_url + scrop.row.audio:'#'">点击播放{{ scrop.row.audio.split('/').pop() }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="video" label="视频展示" min-width="80">
        <template #default="scrop">
          <el-link target="_blank" type="success" :href="!!scrop.row.video?static_url + scrop.row.video:'#'">点击播放{{ scrop.row.video.split('/').pop() }}</el-link>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="120">
        <template #default="scrop">
          <el-button link type="primary" size="small" @click="doEdit(scrop.row.id,scrop.$index)">编辑</el-button>
          <!--          <el-button link type="primary" size="small" @click="doDelete(scrop.row.id,scrop.$index)">删除</el-button>-->
          <el-popconfirm
              confirm-button-text="确认"
              cancel-button-text="取消"
              title="是否确认删除"
              @confirm="doDelete(scrop.row.id,scrop.$index)"
          >
            <template #reference>
              <el-button link type="primary" size="small" @click="">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <!--    分页   -->
    <div style="margin-top: 20px;">
      <el-pagination
          :total="page.totalCount"
          :page-size="page.perPageSize"
          background
          layout=" prev, pager, next, jumper"
          @current-change="handleChangePage"
      ></el-pagination>
    </div>
  </div>


  <!--  黑色幕布  -->
  <div v-show="dialog" class="mask"></div>
  <!--  编辑或保存对话框 -->
  <div v-if="dialog">
    <el-dialog
        v-model="dialog"
        :title="isedit?'编辑':'新建'"
        width="500"
        :before-close="handleClose"
    >
      <!--    <span>这里是编辑/新增表单的地方</span>-->
      <el-form :model="form" label-width="auto" style="max-width: 600px" :rules="rules">
        <el-form-item label="标题" :error="formError.title" prop="title">
          <el-input v-model="form.title"/>
        </el-form-item>

        <!--      <el-form-item label="封面" prop="image">-->
        <!--        <el-input v-model="form.image"/>-->
        <!--      </el-form-item>-->
        <el-form-item label="图片" prop="image">
          <el-upload
              class="avatar-uploader"
              :action="static_url + '/upload/image/'"
              :show-file-list="false"
              :on-success="handleSuccess"
              :before-upload="beforeUpload"
          >
            <img v-if="form.image" :src="static_url + form.image" class="avatar" style="width: 150px;height: 120px"/>
            <img v-if="!form.image" :src="static_url + `/media/image/default.jpg`" class="avatar"
                 style="width: 150px;height: 120px"/>
            <el-icon v-else class="avatar-uploader-icon">
              <Plus/>
            </el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="音频" prop="audio">
          <el-upload
              ref="audioupload"
              class="upload-demo"
              :action="static_url + '/upload/audio/'"
              :limit="1"
              :on-exceed="handleExceedAudio"
              :auto-upload="false"
              :before-upload="beforeAudio"
              :on-success="AudioSuccess"

          >
            <template #trigger>
              <el-button type="primary">选择音频文件</el-button>
            </template>
            <el-button class="ml-3" type="success" @click="UploadAudio">
              确认上传
            </el-button>
            <template #tip>
              <div class="el-upload__tip text-red">
               只限一个文件，且仅限于MP3文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="视频" prop="avatar">
          <el-upload
              ref="videoupload"
              class="upload-demo"
              :action="static_url + '/upload/video/'"
              :limit="1"
              :on-exceed="handleExceedVideo"
              :auto-upload="false"
              :before-upload="beforeVideo"
              :on-success="VideoSuccess"

          >
            <template #trigger>
              <el-button type="primary">选择视频文件文件</el-button>
            </template>
            <el-button class="ml-3" type="success" @click="UploadVideo">
              确认上传
            </el-button>
            <template #tip>
              <div class="el-upload__tip text-red">
                只限一个文件，且仅限于MP3文件
              </div>
            </template>
          </el-upload>
        </el-form-item>

      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialog=false;form={}">取消</el-button>
          <el-button type="primary" @click="doSave(formError)">
            {{ isedit ? '保存' : '确认创建' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {ref, onMounted,computed} from "vue"
import {Search,Printer} from '@element-plus/icons-vue'
import _axios from "@/plugins/axios.js";
import {static_url} from "@/plugins/config.js";
import {userInfoStore} from "@/stores/counter.js";
import {ElMessage, genFileId} from "element-plus";
import * as XLSX from 'xlsx'
const campus_list = ref([])

const compute_label = (id) => {
  console.log("######",id)
  let obj = campus_list.value.find((x)=>x.value===id)
  return obj.label
}

const audioupload = ref()
const videoupload = ref()

const store = userInfoStore()
const loading = ref(false)
const kw = ref("")
const page = ref(({
  totalCount: 100,
  perPageSize: 10,
}))
var datalist = ref([])
const isedit = ref(false)
var form = ref({title:"",image: "/media/userAvatar/default.jpg",audio:"",video:""})  // 绑定对话框的表单字段内容
var rules = ref({
  title: [{
    required: true, message: "标题不能为空"
  }],
  birth: [{
    required: true, message: "生日不能为空"
  }],
  // image: [{
  //   required: true, message: "昵称不能为空"
  // }],
  campus: [{
    required: true, message: "校区不能为空"
  }]
})
var formError = ref({
  title: "",
  author: "",
  price: ""
})
var isLoading = ref(true) // 是否正在加载
var dialog = ref(false)
const editid = ref(null)
const editidx = ref(null)
const selectedList = ref({})
onMounted(function (e) {
  fetchDatalist()
  // fetchCampuslist()
  // _axios.get(`/api/book/`, {
  //   headers: {
  //     "token": store.token
  //   },
  // }).then(function (res) {
  //   datalist.value = res.data.data.results
  //   page.value.totalCount = res.data.data.count
  //   console.log("datalist.value", datalist.value)
  // })
})

function handleSelectionChange(val) {
  selectedList.value = val
  console.log("val", selectedList.value)
}

// 打开新建版dialog
function doCreate() {
  //点击新增按钮
  isedit.value = false
  dialog.value = true

}


// 打开编辑版dialog
function doEdit(id, idx) {
  // 编辑
  console.log(123, datalist.value[idx])
  // form.value = datalist.value[idx]  // js的赋值和python一样，是一个指向关系
  form.value = {...datalist.value[idx]}

  editid.value = id
  editidx.value = idx
  isedit.value = true
  dialog.value = true
}

// 执行保存逻辑（新增&删除）
function doSave(e) {
  // console.log("待提交数据:", form.value)
  // console.log("错误信息:", e)
  // return 0

  if (!!isedit.value) {
    // 编辑逻辑
    // console.log("编辑")
    // console.log(form.value)
    _axios.put(`/api/medias/${editid.value}/`, {
      ...form.value
    }, {
      headers: {
        token: store.token
      }
    }).then(function (res) {
      if (res.data.code === 0) {
        ElMessage.success("修改成功")
        datalist.value[editidx.value] = res.data.data
        form.value = {title:"",image: "/media/userAvatar/default.jpg",audio:"",video:""}
        dialog.value = false

      } else {
        dialog.value = false
        form.value = {title:"",image: "/media/userAvatar/default.jpg",audio:"",video:""}
        ElMessage.error("操作异常")
      }
    })


  } else {
    // 新建逻辑
    _axios.post("/api/medias/", {
      ...form.value
    }, {
      headers: {
        token: store.token
      }
    }).then(function (res) {
      if (res.data.code === 0) {
        dialog.value = false
        // datalist.value.splice(0, 0, res.data.data);
        datalist.value.push(res.data.data);
        form.value = {title:"",image: "/media/userAvatar/default.jpg",audio:"",video:""}
        Object.keys(formError.value).forEach((x) => {
          formError.value[x] = ""
        })
        ElMessage.success('创建成功!');
      } else {
        ElMessage.error('创建失败!');
      }
    })
  }
}

// 执行删除逻辑
function doDelete(id, idx) {
  console.log("删除", id, idx)
  _axios.delete(`/api/medias/${id}/`, {
    headers: {
      token: store.token
    }
  }).then(function (res) {
    if (res.data.code === 0) {
      ElMessage.success("删除成功")
      datalist.value.splice(idx, 1)
    } else {
      ElMessage.error("操作异常!")
    }
  })
}

// 新增/编辑dialog 窗口关闭的回调函数
function handleClose() {
  // dialog 关闭 清空form
  console.log("错误信息", formError.title)
  dialog.value = false
  Object.keys(formError.value).forEach((x) => {
    formError.value[x] = ""
  })
  console.log(formError.value)
  form.value = {title:"",image: "/media/userAvatar/default.jpg",audio:"",video:""}
}

// 图片上传成功的回调函数
function handleSuccess(res) {
  form.value.image = res.data.path
}

// 执行搜素哦
function doSearch() {
  console.log("kw.value", kw.value)
  _axios.get(`/api/medias/?kw=${kw.value}`, {
    headers: {
      token: store.token
    }
  }).then(function (res) {
    if (res.data.code === 0) {
      ElMessage.success(!!res.data.data.results.length ? "查询成功" : "空空如也")
      datalist.value = res.data.data.results
      kw.value = ""

    } else {
      ElMessage.error("查询异常")
    }
  })


}

// 上传前夕
const beforeUpload = (rawFile) => {
  if (rawFile.type !== 'image/jpeg') {
    ElMessage.error('必须是图片格式!');
    return false;
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('图片大小不能大于2MB');
    return false;
  }
  return true;
};

// 批量删除
function doDeleteSelected(e) {
  let toDeleteList = selectedList.value.map((x) => x.id)          // 待删除条目的id
  _axios.delete("/api/medias/", {
    data: {id_list: JSON.stringify(toDeleteList)},
    headers: {
      token: store.token
    }

  }).then(function (res) {
    if (res.data.code === 0) {
      // 反向获取索引
      // let idxlist= datalist.value.map((item)=>datalist.value.indexOf(item))
      // idxlist.forEach((x)=>datalist.value.splice(x,1)
      datalist.value = datalist.value.filter((item) => !selectedList.value.includes(item))
      ElMessage.success("批量删除成功")
    } else {
      ElMessage.error("请求异常")
    }
  })
}

// 换页操作的回调函数
function handleChangePage(num) {
  console.log("当前点击了",num)
  fetchDatalist(num)
}

// 获取数据
function fetchDatalist(num) {
  loading.value = true
  _axios.get("/api/medias/", {params: {page: num ? num : 1},headers:{token:store.token}}).then(function (res) {
    if (res.data.code === 0) {
      datalist.value = res.data.data.results
      page.value = {
        totalCount: res.data.data.count,
        // perPageSize: res.data.data.perpagecount,
      }
      loading.value = false // 加载完毕
    } else{
      console.log("请求异常",res)
    }
  }).catch(function (errors) {
    console.log(errors)
  })
}



// 导出excel
let exportSelectedSub=()=> {
  // 创建一个XLSX工作簿（workbook）
  const ws = XLSX.utils.json_to_sheet(selectedList.value);
  const wb = XLSX.utils.book_new();
  // 将工作表（worksheet）添加到工作簿中，命名为'Sheet1'
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
  // 使用XLSX库的writeFile函数将工作簿保存为XLSX文件并提供下载
  XLSX.writeFile(wb, 'tableData.xlsx');
}




// 公共部分



// 音频上传部分
function handleExceedAudio(files){
  // 档上传文件数超出限制，执行此函数
  audioupload.value.clearFiles();
  const file = files[0];
  file.uid = genFileId();
  audioupload.value.handleStart(file);
}
function UploadAudio(e){
if(audioupload.value){
  audioupload.value.submit()
}
}
function beforeAudio(rawFile){
  console.log("rawFile,",rawFile)
//  audio/mpeg
  if (rawFile.type !== 'audio/mpeg') {
    ElMessage.error('必须是mp3格式!');
    return false;
  } else if (rawFile.size / 1024 / 1024 > 50) {
    ElMessage.error('音频大小不能大于50MB');
    return false;
  }
  return true;
}
function AudioSuccess(res){
  form.value.audio = res.data.path
}

// 视频上传部分
function handleExceedVideo(files){
  // 档上传文件数超出限制，执行此函数
  audioupload.value.clearFiles();
  const file = files[0];
  file.uid = genFileId();
  audioupload.value.handleStart(file);
}

function UploadVideo(e){
  if(videoupload.value){
    videoupload.value.submit()
  }
}
function beforeVideo(rawFile){
  if (rawFile.type !== 'video/mp4') {
    ElMessage.error('必须是mp4格式!');
    return false;
  } else if (rawFile.size / 1024 / 1024 > 50) {
    ElMessage.error('视频大小不能大于50MB');
    return false;
  }
  return true;
}
function VideoSuccess(res){
  form.value.video = res.data.path
}


</script>


<style scoped>
.mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: black;
  opacity: 0.8;
  z-index: 998;
}

</style>