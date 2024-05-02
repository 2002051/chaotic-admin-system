<template>
  <div style="font-size: 20px  "><strong>简历管理（pdf格式）</strong></div>
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

    <el-button v-if="!!selectedList.length" :icon="Printer" @click="exportSelectedSub"
               style="margin-left: 10px;background-color: #eaeaea">导出
    </el-button>

  </div>

  <div v-loading="loading">
    <el-table :data="datalist" style="width: 100%;height: 95%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <!--      <el-table-column type="index" label="" :index="indexMethod" />-->
      <el-table-column prop="id" label="ID" width="80"/>
      <el-table-column prop="name" label="名字" width="180"/>
      <!--      <el-table-column prop="age" label="年龄" min-width="180" wwidth="180">-->
      <!--        <template #default="scrop">-->
      <!--          &lt;!&ndash;          <el-image style="width: 100px; height: 100px" :src="static_url + scrop.row.image" :fit="scrop.$index"/>&ndash;&gt;-->
      <!--          <el-image style="width: 100px; height: 100px" :src="static_url + scrop.row.image"/>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column prop="age" label="年龄" width="180"/>
      <el-table-column prop="education_dict.v" label="学历" width="180"/>
      <el-table-column prop="attachment" label="简历附件" min-width="180">
        <template #default="scrop">
          <!--          此处预览我推荐使用云存储-->
          <el-link :href="static_url + scrop.row.attachment" target="_blank" type="default">
            {{ scrop.row.attachment.split('/').pop() }}
          </el-link>
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
        <el-form-item label="名字" :error="formError.name"  prop="name">
          <el-input v-model="form.name"/>
        </el-form-item>

        <el-form-item label="年龄" :error="formError.age" prop="age">
          <el-input-number v-model="form.age" :min="1" :max="200"/>
        </el-form-item>

        <el-form-item label="学历" :error="formError.education" prop="education">

          <el-select-v2
              v-model="form.education"
              :options="options"
              placeholder="选择学历"
              size="large"
              style="width: 240px"

          />

        </el-form-item>

        <el-form-item label="简历附件" :error="formError.attachment" prop="attachment">
          <el-upload
              class="upload-demo"
              drag
              :action="static_url + `/upload/biographical/`"
              multiple
              :on-success="handleSuccess"
              :before-upload="beforeUpload"
              limit = 1
          >
            <el-icon class="el-icon--upload"><UploadFilled/></el-icon>
            <div class="el-upload__text">
             拖动上传或者 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                只能上传pdf文件
              </div>
            </template>
          </el-upload>
        </el-form-item>

      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialog=false;form={}">取消</el-button>
          <el-button v-if="formIsFull()" type="primary" @click="doSave()">
            {{ isedit ? '保存' : '确认创建' }}
          </el-button>

          <el-button v-if="!formIsFull()" type="primary" @click="doSave" disabled>
            {{ isedit ? '保存' : '确认创建' }}
          </el-button>


        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue"
import {Search, Printer,UploadFilled} from '@element-plus/icons-vue'
import _axios from "@/plugins/axios.js";
import {static_url} from "@/plugins/config.js";
import {userInfoStore} from "@/stores/counter.js";
import {ElMessage} from "element-plus";
import * as XLSX from 'xlsx'

const store = userInfoStore()
const loading = ref(false)
const kw = ref("")
const page = ref(({
  totalCount: 100,
  perPageSize: 10,
}))
var datalist = ref([])
const isedit = ref(false)
var form = ref({
  name: "",
  age: "",
  education: "",
  attachment: "/media/biographical/default.pdf"
})
var rules = ref({
  name: [{
    required: true, message: "名字不能为空"
  }],
  age: [{
    required: true, message: "年龄不能为空"
  }],
  education: [{
    required: true, message: "学历不能为空"
  }],
  attachment: [{
    required: true, message: "附件不能为空"
  }]
})
var formError = ref({
  name: "",
  age: "",
  education: "",
  attachment: ""
})
var isLoading = ref(true) // 是否正在加载
var dialog = ref(false)
const editid = ref(null)
const editidx = ref(null)
const selectedList = ref({})
// const options = ref({
//   1:"小学",2:"初中",3:"高中", 4:"本科", 5:"研究生",  6:"博士",  7:"其它",
// })
const options = ref([{value: 1, label: "小学"}, {value: 2, label: "初中"}, {value: 3, label: "高中"},
  {value: 4, label: "本科"}, {value: 5, label: "研究生"}, {value: 6, label: "博士"}, {value: 7, label: "其它"}])

onMounted(function (e) {
  fetchDatalist()

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
  // form.value = datalist.value[idx]  // js的赋值和python一样，是一个指向关系
  form.value = {...datalist.value[idx]}
  delete form.value.education_dict
  form.value.education = datalist.value[idx].education_dict.k
  console.log("doEdit", form.value)
  editid.value = id
  editidx.value = idx
  isedit.value = true
  dialog.value = true
}

// 执行保存逻辑（新增&删除）
function doSave() {
  // console.log("保存:", form.value)
  // console.log("错误信息:", formError.value)
  console.log("待提交内容", form.value, formError.value)
  // return 0


  if (!!isedit.value) {
    // 编辑逻辑
    // console.log("编辑")
    // console.log(form.value)
    _axios.put(`/api/biographical/${editid.value}/`, {
      ...form.value
    }, {
      headers: {
        token: store.token
      }
    }).then(function (res) {
      if (res.data.code === 0) {
        ElMessage.success("修改成功")
        datalist.value[editidx.value] = res.data.data
        form.value = {
          name: "",
          age: "",
          education: "",
          attachment: "/media/biographical/default.pdf"
        }
        dialog.value = false

      } else {
        dialog.value = false
        form.value = {
          name: "",
          age: "",
          education: "",
          attachment: "/media/biographical/default.pdf"
        }
        ElMessage.error("操作异常")
      }
    })

  } else {
    // 新建逻辑
    _axios.post("/api/biographical/", {
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
        form.value = {
          name: "",
          age: "",
          education: "",
          attachment: "/media/biographical/default.pdf"
        }
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
  _axios.delete(`/api/biographical/${id}/`, {
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
  form.value = {
    name: "",
    age: "",
    education: "",
    attachment: "/media/biographical/default.pdf"
  }
}

// 图片上传成功的回调函数
function handleSuccess(res) {
  console.log(res)
  form.value.attachment = res.data.path
  console.log(form.value)
}

// 执行搜素哦
function doSearch() {
  console.log("kw.value", kw.value)
  _axios.get(`/api/biographical/?kw=${kw.value}`, {
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
  console.log("文件类型",rawFile.type)
  if (rawFile.type !== 'application/pdf') {
    ElMessage.error('必须是pdf格式的文件!');
    return false;
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('文件大小不能大于2MB');
    return false;
  }
  return true;
};

// 批量删除
function doDeleteSelected(e) {
  let toDeleteList = selectedList.value.map((x) => x.id)          // 待删除条目的id
  _axios.delete("/api/biographical/", {
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
  console.log("当前点击了", num)
  fetchDatalist(num)
}

// 获取数据
function fetchDatalist(num) {
  loading.value = true
  _axios.get("/api/biographical/", {params: {page: num ? num : 1}, headers: {token: store.token}}).then(function (res) {
    if (res.data.code === 0) {
      datalist.value = res.data.data.results
      page.value = {
        totalCount: res.data.data.count,
        // perPageSize: res.data.data.perpagecount,
      }
      loading.value = false // 加载完毕
    } else {
      console.log("请求异常", res)
    }
  }).catch(function (errors) {
    console.log(errors)
  })
}

// 导出excel
let exportSelectedSub = () => {
  // 创建一个XLSX工作簿（workbook）
  const ws = XLSX.utils.json_to_sheet(selectedList.value);
  const wb = XLSX.utils.book_new();
  // 将工作表（worksheet）添加到工作簿中，命名为'Sheet1'
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
  // 使用XLSX库的writeFile函数将工作簿保存为XLSX文件并提供下载
  XLSX.writeFile(wb, 'tableData.xlsx');
}

function formIsFull() {
  for(let key in form.value){
    if(!form.value[key]){
      return false
    }
  }
  return true
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