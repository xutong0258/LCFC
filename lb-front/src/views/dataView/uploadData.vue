<template>
  <el-dialog
    title="人工上传issue"
    width="1393px"
    v-model="visible"
    append-to-body
    :before-close="closeCategory"
  >
    <div class="container">
      <el-row :gutter="24">
        <el-col :span="18">
          <el-form ref="dataForm" :model="dataForm" :rules="rules" label-position="left" label-width="150px"
                   :validate-on-rule-change="false">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="issue标题" prop="title">
                  <el-input v-model="dataForm.title"/>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="issue类型" prop="issueType">
                  <el-select v-model="dataForm.issueType" class="filter-item"
                             @change="handleTypeChange"
                  >
                    <el-option
                      v-for="item in optionsTypes"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="24">
                <el-form-item label="详细描述" prop="description">
                  <el-input v-model="dataForm.description" placeholder="请详细描述issue的内容、复现步骤、影响范围等..."
                            type="textarea"/>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="优先级">
                  <el-select v-model="dataForm.priority" class="filter-item"
                             @change="handleTypeChange"
                  >
                    <el-option
                      v-for="item in optionsPriorities"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="预期解决日期">
                  <el-date-picker
                    v-model="dataForm.expectedResolveDate"
                    type="date"
                    placeholder="预期解决日期"
                    style="width: 100%"
                    date-format
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="24">
                <el-form-item label="附件上传">
                  <el-upload
                    multiple
                    drag
                    :action="uploadFileUrl"
                    :before-upload="handleBeforeUpload"
                    :file-list="fileList"
                    :on-error="handleUploadError"
                    :on-success="handleUploadSuccess"
                    :on-remove="handleRemove"
                    :show-file-list="true"
                    :headers="headers"
                    class="upload-file-uploader"
                    ref="fileUpload">

                    <div class="el-upload__text" style="text-align: center">
                      <img src="@/assets/file-link.png">
                      <div>
                        拖放文件到此处，或
                      </div>
                      <div
                        style="border: 1px solid #409EFF;width: 90px;border-radius: 4px;display: flex;justify-content: center">
                        <em>选择文件</em></div>
                      <div>(支持 .jpg, .png, .pdf, .zip 等格式，单个文件不超过10MB)</div>
                    </div>
                  </el-upload>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="24">
              <el-col :span="24">
                <el-form-item label="标签">
                  <el-input-tag
                    v-model="dataForm.tags"
                    placeholder="输入标签"
                    tag-type="primary"
                  />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-col>

        <el-col :span="6">
          <div class="card-top">
            <img src="@/assets/upload-img.png">
            最近上传的issue
          </div>
          <div class="top-info">

            <div class="info-cards" :class="param.pageSize>3?'info-ex':''">
              <div class="info-card" v-for="(item,index)  in issueList">
                <div class="info-title">{{ item.title }}</div>
                <div class="info-desc">
                  <div class="info-img"><img
                    src="@/assets/info-time.png">{{ dayjs(item.createTime).format('YYYY-MM-DD HH:mm:ss') }}
                  </div>
                  <div v-if="item.status=='pending'" class="info-status status-waiting">待处理</div>
                  <div v-if="item.status=='completed'" class="info-status status-finish">已处理</div>
                  <div v-if="item.status=='diagnosing'" class="info-status status-processing">处理中</div>
                </div>
              </div>
            </div>
            <div v-if="total<=3" @click="toAll" class="info-more">查看全部 <img src="@/assets/file-more.png"></div>
            <div v-else @click="toput" class="info-more">收起全部 <img src="@/assets/file-more.png"></div>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col style="display: flex;justify-content: center;margin-top: 45px">
          <el-button @click="onSave">保存草稿</el-button>
          <el-button type="primary">提交issue</el-button>
        </el-col>
      </el-row>
    </div>
  </el-dialog>
</template>

<script>
import { useGet, usePost } from "@/utils/request.js";
import { ElMessage } from "element-plus";
import dayjs from 'dayjs'

export default {
  name: "UploadIssueData",  // 组件名首字母大写规范
  props: {
    modelValue: {  // 固定属性名，v-model 默认绑定这个
      type: Boolean,  // 类型是布尔值（控制显示/隐藏）
      default: false  // 默认隐藏
    }
  },
  data() {
    return {
      visible: this.modelValue,
      dataForm: {},
      rules: {
        title: [
          { required: true, message: '标题不能为空！' }
        ],
        issueType: [
          { required: true, message: '类型不能为空！' }]
        ,
        description: [
          { required: true, message: '详细描述不能为空！' }
        ]
      },
      optionsPriorities: [],
      optionsTypes: [],
      fileList: [],
      headers: { Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjM3ZTVlZGYzLWRjNjUtNDUxMC04MWQwLTY3NDQ5NDIyZjk4YiIsImxvZ2luX2luZm8iOm51bGwsImV4cCI6MjAxOTYyNzM5Nn0.IWYvHGmrcjngTwBI4eXvlcHDWNuhk_nTPH1EwFpW15Y" }, // 设置上传的请求头部,
      uploadFileUrl: '/api/system/issue/attachment/upload',
      uploadList: [],
      // issue_id: 123,
      issueList: [],
      total: 0,
      param: {
        pageNum: 1,
        pageSize: 3
      },
      attachmentIds:[]
    }
  },
  watch: {
    modelValue(newVal) {
      this.visible = newVal;
    },
    // 3. 监听子组件 visible 变化，同步给父组件（比如子组件关闭弹窗）
    visible(newVal) {
      this.$emit('update:modelValue', newVal);  // 固定事件名，触发后父组件 v-model 会更新
    }
  },
  created() {
    this.attachmentIds=[]
    this.getOptionsPriorities()
    this.getOptionsTypes()
    this.getIssueList(1)
    // this.uploadFileUrl=this.uploadFileUrl+'?issue_id=1'
  },
  methods: {
    dayjs,
    // 实现关闭逻辑
    closeCategory() {
      this.visible = false;
    }, handleTypeChange() {
    },
    //获取优先级
    getOptionsPriorities() {
      useGet('/system/issue/options/priorities', {}).then((res) => {
        console.log(res)
        const { data, success, message } = res
        if (success) {
          this.optionsPriorities = data || {}
        } else {
          ElMessage.error(message || '请求失败')
        }
      })
    },
    //获取类型
    getOptionsTypes() {
      useGet('/system/issue/options/types', {}).then((res) => {
        console.log(res)
        const { data, success, message } = res
        if (success) {
          this.optionsTypes = data || {}
        } else {
          ElMessage.error(message || '请求失败')
        }
      })
    },
    //保存草稿
    onSave() {
      const payload = {}
      payload.title = this.dataForm.title
      payload.priority = this.dataForm.priority
      payload.issueType = this.dataForm.issueType
      payload.description = this.dataForm.description
      payload.expectedResolveDate = dayjs(this.dataForm.expectedResolveDate).format('YYYY-MM-DD')
      payload.tags = this.dataForm.tags
      payload.attachmentlds = this.attachmentIds
      usePost('/system/issue', payload).then((res) => {
        console.log(res)
        const { data, success, message } = res
        if (success) {

          ElMessage.success(message || '保存成功')

        } else {
          ElMessage.error(message || '请求失败')
        }
      })
    },
    // 上传前校检格式和大小
    handleBeforeUpload(file) {
      // 校检文件类型
      if (this.fileType) {
        let fileExtension = "";
        if (file.name.lastIndexOf(".") > -1) {
          fileExtension = file.name.slice(file.name.lastIndexOf(".") + 1);
        }
        const isTypeOk = this.fileType.some((type) => {
          if (file.type.indexOf(type) > -1) return true;
          if (fileExtension && fileExtension.indexOf(type) > -1) return true;
          return false;
        });
        if (!isTypeOk) {
          ElMessage.error(`文件格式不正确, 请上传${ this.fileType.join("/") }格式文件!`);
          return false;
        }
      }
      // 校检文件大小
      if (this.fileSize) {
        const isLt = file.size / 1024 / 1024 < this.fileSize;
        if (!isLt) {
          ElMessage.error(`上传文件大小不能超过 ${ this.fileSize } MB!`);
          return false;
        }
      }
      ElMessage.warning("正在上传文件，请稍候...");
      this.number++;
      return true;
    },// 上传失败
    handleUploadError(err) {
      ElMessage.error("上传图片失败，请重试");
    },// 上传成功回调
    handleUploadSuccess(res, file) {
      if (res.code === 200) {

        const attachmentId = res.data?.attachmentId; // 使用可选链操作符避免报错

        if (attachmentId) {
          this.attachmentIds.push(attachmentId);
          // this.fileList.push({
          //   name: file.name,
          //   url: res.data.url,
          //   uid: file.uid,
          // });
        } else {
          console.error('未找到 attachmentId', res.data);
          // 处理没有获取到ID的情况
          this.$message.error('文件上传成功，但未获取到文件ID');
        }
      } else {
        this.number--;
        this.$refs.fileUpload.handleRemove(file);
      }
    },
    // 获取文件名称
    getFileName(name) {
      if (name.lastIndexOf("/") > -1) {
        return name.slice(name.lastIndexOf("/") + 1);
      } else {
        return "";
      }
    }, handleRemove(file, fileList) {
      let index = this.fileList.indexOf(file);
      this.fileList.splice(index, 1);
    },//获取列表
    getIssueList(flag) {
      const payload = {}
      payload.pageNum = this.param.pageNum
      payload.pageSize = this.param.pageSize;
      useGet('/system/issue/list', payload).then((res) => {
        const { data, success, message } = res
        if (success) {
          this.issueList = data.rows || []
          this.total = data.total
        } else {
          ElMessage.error(message || '请求失败')
        }
      })
    }, toAll() {
      this.param.pageNum = 1
      this.param.pageSize = 20
      this.getIssueList()
    }, toput() {
      this.param.pageNum = 1
      this.param.pageSize = 3
      this.getIssueList()
    }

  }
}
</script>
<style scoped>
/* 1. 定位弹窗根节点，设置整体渐变背景和高度 */
:deep(.custom-dialog) {
  height: 873px !important;
  /* 渐变背景覆盖整个弹窗（包括头部和内容区） */
  background: linear-gradient(180deg, #D2E1FF 0%, #FFFFFF 9%, #FFFFFF 100%) !important;
  /* 清除弹窗默认的白色背景（关键！避免默认样式覆盖渐变） */
  --el-dialog-bg-color: transparent !important;
}

/* 2. 弹窗内容区：继承背景，设置内边距和高度 */
:deep(.custom-dialog .el-dialog__body) {
  padding: 20px;
  margin: 0;
  /* 高度 = 弹窗总高 - 头部高度（60px 是 Element Plus 头部默认高度，可按需调整） */
  height: calc(100% - 60px) !important;
  background: transparent !important; /* 确保继承父级渐变，不单独加背景 */
  overflow: auto; /* 内容超出时滚动，避免页面错乱 */
}

/* 3. 弹窗头部：清除默认白色背景，继承渐变 */
:deep(.custom-dialog .el-dialog__header) {
  background: transparent !important;
  padding: 16px 20px; /* 可选：调整头部内边距，和内容区对齐 */
}

.container {
  padding: 20px;
  box-sizing: border-box;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
}

:deep(.el-form-item__label) {
  width: 107px !important;
}

.upload-file-uploader {
  margin-bottom: 5px;
  width: 100%;
}

.upload-file-list .el-upload-list__item {
  border: 1px solid #e4e7ed;
  line-height: 2;
  margin-bottom: 10px;
  position: relative;
}

.upload-file-list .ele-upload-list__item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: inherit;
}

.ele-upload-list__item-content-action .el-link {
  margin-right: 10px;
}

.el-upload__text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  img {
    width: 24px;
    height: 24px;
  }
}

.card-top {
  img {
    width: 16px;
    height: 16px;
    margin-right: 8px;
  }

  font-family: AlibabaPuHuiTi;
  font-size: 14px;
  font-weight: normal;
  line-height: 21px;
  display: flex;
  align-items: center;
  letter-spacing: 0px;
  color: #333333;
  margin-bottom: 16px;
}

.info-ex {
  box-sizing: border-box;
  height: 400px;
  overflow: hidden;
  overflow-y: scroll;
}

.info-cards {
  border-bottom: 1px solid #EAEAEA;

  .info-card {
    margin-bottom: 12px;
    background-color: #F5F7FA;
    border-radius: 4px;
    padding: 8px;


  }

  .info-title {
    font-family: 'AlibabaPuHuiTi';
    font-size: 14px;
    font-weight: normal;
    line-height: 21px;
    display: flex;
    align-items: center;
    color: #333333 !important;
  }

  .info-desc {
    padding-top: 4px;
    display: flex;
    font-family: 'AlibabaPuHuiTi';
    font-size: 12px;
    font-weight: normal;
    line-height: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    letter-spacing: 0px;
    color: #999999;

  }

  .info-img {
    display: flex;
    align-items: center;

    img {
      width: 12px;
      height: 12px;
      margin-right: 4px;
    }
  }

  .status-waiting {
    color: #FAAD14;
  }

  .status-finish {
    color: #52C41A;
  }

  .status-processing {
    color: #1677FF;
  }
}

.info-more {
  padding-top: 12px;
  font-family: AlibabaPuHuiTi;
  font-size: 14px;
  font-weight: normal;
  line-height: 21px;
  display: flex;
  align-items: center;
  color: #1677FF;
  justify-content: center;

  img {
    width: 6px;
    height: 11px;
    margin-left: 4px;
  }
}
</style>
