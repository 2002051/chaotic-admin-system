<template>
  <div>
    <el-button type="primary" @click="doCreate">新增</el-button>
    <el-button>批量删除</el-button>
    <span style="margin-left: 24px;">
    <el-input v-model="kd" style="width: 240px;margin-left: 12px;" placeholder="请输入关键字"/>
      <el-button type="primary">
             <el-icon>
                <Search/>
              </el-icon>
      </el-button>
  </span>
  </div>

  <div>
    <el-table :data="datalist" style="width: 100%;height: 95%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <!--      <el-table-column type="index" label="" :index="indexMethod" />-->
      <el-table-column prop="id" label="ID" idth="180"/>
      <el-table-column prop="title" label="标题" width="180"/>
      <el-table-column prop="image" label="封面图片" min-width="180" wwidth="180">
        <template #default="scrop">
          <el-image style="width: 100px; height: 100px" :src="static_url + scrop.row.image" :fit="scrop.$index"/>
        </template>
      </el-table-column>
      <el-table-column prop="author" label="作者" width="180"/>
      <el-table-column prop="price" label="价格(分)" width="180"/>
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

        <el-form-item label="作者" :error="formError.author" prop="author">
          <el-input v-model="form.author"/>
        </el-form-item>

        <!--      <el-form-item label="封面" prop="image">-->
        <!--        <el-input v-model="form.image"/>-->
        <!--      </el-form-item>-->
        <el-form-item label="上传封面" prop="image">
          <el-upload
              class="avatar-uploader"
              :action="static_url + '/upload/bookimg/'"
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
          >
            <img v-if="form.image" :src="static_url + form.image" class="avatar" style="width: 150px;height: 120px"/>
            <img v-if="!form.image" :src="static_url + `/media/book_img/default.jpg`" class="avatar"
                 style="width: 150px;height: 120px"/>
            <el-icon v-else class="avatar-uploader-icon">
              <Plus/>
            </el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="价格(分)" :error="formError.price" prop="price">
          <el-input-number v-model="form.price" :min="1" :max="10000"/>

        </el-form-item>

      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialog=false,form={}">取消</el-button>
          <el-button type="primary" @click="doSave">
            {{ isedit ? '保存' : '确认创建' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {ref, onMounted} from "vue"
import {Search} from '@element-plus/icons-vue'
import _axios from "@/plugins/axios.js";
import {static_url} from "@/plugins/config.js";
import {userInfoStore} from "@/stores/counter.js";
import {ElMessage} from "element-plus";

const kd = ref("")
const isedit = ref(false)

var form = ref({image: "/media/book_img/default.jpg"})  // 绑定对话框的表单字段内容
var rules = ref({
  title: [{
    required: true, message: "昵称不能为空"
  }],
  author: [{
    required: true, message: "作者不能为空"
  }],
  // image: [{
  //   required: true, message: "昵称不能为空"
  // }],
  price: [{
    required: true, message: "价格不能为空"
  }]
})
var formError = ref({
  title: "",
  author: "",
  price: ""
})
var datalist = ref([])
const store = userInfoStore()
var isLoading = ref(true) // 是否正在加载
var dialog = ref(false)

const editid = ref(null)
const editidx = ref(null)

onMounted(function (e) {
  _axios.get(`/api/book/`, {
    headers: {
      "token": store.token
    },
  }).then(function (res) {
    datalist.value = res.data.data.results
    console.log("datalist.value", datalist.value)
  })
})

function handleSelectionChange(val) {
  console.log("val", val)
}


function doCreate() {
  //点击新增按钮
  isedit.value = false
  dialog.value = true

}

function doEdit(id, idx) {
  // 编辑
  console.log(123, datalist.value[idx])
  form.value = datalist.value[idx]
  editid.value = id
  editidx.value = idx
  isedit.value = true
  dialog.value = true
}

function doSave() {
  // console.log("保存:", form.value)
  // console.log("错误信息:", formError.value)
  if (!!isedit.value) {
    // 编辑逻辑
    // console.log("编辑")
    // console.log(form.value)
    _axios.put(`/api/book/${editid.value}/`, {
      ...form.value
    }, {
      headers: {
        token: store.token
      }
    }).then(function (res) {
      if (res.data.code === 0) {
        ElMessage.success("修改成功")
        datalist.value[editidx] = res.data.data
        form.value = {image: "/media/book_img/default.jpg"}
        dialog.value = false

      } else {
        dialog.value = false
        form.value = {image: "/media/book_img/default.jpg"}
        ElMessage.error("操作异常")
      }
    })


  } else {
    // 新建逻辑
    _axios.post("/api/book/", {
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
        form.value = {image: "/media/book_img/default.jpg"}
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

function doDelete(id, idx) {
  console.log("删除", id, idx)
  _axios.delete(`/api/book/${id}/`, {
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

function handleClose() {
  // dialog 关闭 清空form
  console.log("错误信息", formError.title)
  dialog.value = false
  Object.keys(formError.value).forEach((x) => {
    formError.value[x] = ""
  })
  console.log(formError.value)
  form.value = {}
}


function handleAvatarSuccess(res) {
  form.value.image = res.data.path
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