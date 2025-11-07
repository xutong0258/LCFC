<template>
  <div class="course-upload-file">
    <el-upload
      multiple
      drag
      :action="uploadFileUrl"
      :before-upload="handleBeforeUpload"
      :file-list="fileList"
      :limit="limit"
      :on-error="handleUploadError"
      :on-exceed="handleExceed"
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
  </div>
</template>

<script>
import { getAccessToken } from "@/utils/auth";

export default {
  name: "FileUpload",
  props: {
    // 值
    value: [String, Object, Array],
    // 数量限制
    limit: {
      type: Number,
      default: 10,
    },
    // 大小限制(MB)
    fileSize: {
      type: Number,
      default: 1024,
    },
    // 文件类型, 例如['png', 'jpg', 'jpeg']
    fileType: {
      type: Array,
      default: () => ["doc", "xls", "ppt", "txt", "pdf"],
    },
    // 是否显示提示
    isShowTip: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      number: 0,
      uploadList: [],
      baseUrl: process.env.VUE_APP_BASE_API,
      uploadFileUrl: process.env.VUE_APP_BASE_API + "/admin-api/infra/file/upload", // 请求地址
      headers: { Authorization: "Bearer " + getAccessToken() }, // 设置上传的请求头部
      fileList: [],
    };
  },
  watch: {
    value: {
      handler(val) {
        if (val) {
          let temp = 1;
          // 首先将值转为数组
          const list = Array.isArray(val) ? val : this.value.split(',');
          // 然后将数组转为对象数组
          this.fileList = list.map(item => {
            if (typeof item === "string") {
              item = { name: item, url: item };
            }
            item.uid = item.uid || new Date().getTime() + temp++;
            return item;
          });
        } else {
          this.fileList = [];
          return [];
        }
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    // 是否显示提示
    showTip() {
      return this.isShowTip && (this.fileType || this.fileSize);
    },
  },
  methods: {
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
          this.$modal.msgError(`文件格式不正确, 请上传${this.fileType.join("/")}格式文件!`);
          return false;
        }
      }
      // 校检文件大小
      if (this.fileSize) {
        const isLt = file.size / 1024 / 1024 < this.fileSize;
        if (!isLt) {
          this.$modal.msgError(`上传文件大小不能超过 ${this.fileSize} MB!`);
          return false;
        }
      }
      this.$modal.loading("正在上传文件，请稍候...");
      this.number++;
      return true;
    },
    // 文件个数超出
    handleExceed() {
      this.$modal.msgError(`上传文件数量不能超过 ${this.limit} 个!`);
    },
    // 上传失败
    handleUploadError(err) {
      this.$modal.msgError("上传文件失败，请重试");
      this.$modal.closeLoading()
    },
    // 上传成功回调
    handleUploadSuccess(res, file) {
      if (res.code === 0) {
        console.log("上传文件成功：===========" + JSON.stringify(res));
        const name = res.data;
        const type = this.getFileType(name);
        this.uploadList.push({ name: res.data, url: res.data, type: type, file: file });
        this.uploadedSuccessfully();
      } else {
        console.log("上传文件失败：===========" + JSON.stringify(res));
        this.number--;
        this.$modal.closeLoading();
        this.$modal.msgError(res.msg);
        this.$refs.fileUpload.handleRemove(file);
        this.uploadedSuccessfully();
      }
    },
    handleRemove(file, fileList) {
      let index = this.fileList.indexOf(file);
      this.fileList.splice(index, 1);
      this.$emit("fileList", this.listToString(this.fileList));
    },
    clearData() {
      this.fileList = [];
      this.uploadList = [];
      this.number = 0;
    },
    handleDelete(index) {
      console.log("删除一个上传文件：===========" + index);
      this.fileList.splice(index, 1);
      this.$emit("fileList", this.listToString(this.fileList));
    },
    // 获取视频时长
    async getVideoDuration(file) {
      return new Promise((resolve) => {
        const video = document.createElement('video');
        video.src = URL.createObjectURL(file);
        video.onloadedmetadata = () => {
          URL.revokeObjectURL(video.src);
          resolve(Math.floor(video.duration));
        };
      });
    },
    // 上传结束处理
    async uploadedSuccessfully() {
      console.log("上传文件结束：===========" + this.number);
      console.log("上传文件结束：===========uploadList" + JSON.stringify(this.uploadList));
      if (this.number > 0 && this.uploadList.length === this.number) {
        console.log("上传文件结束：===========fileList" + JSON.stringify(this.fileList));

        // 处理视频文件获取时长
        const videoTypes = ['mp3', 'mp4', 'flv'];
        for (const item of this.uploadList) {
          if (videoTypes.includes(item.type) && item.file.raw) {
            try {
              const duration = await this.getVideoDuration(item.file.raw);
              item.duration = duration;
            } catch (error) {
              console.error('获取视频时长失败:', error);
            }
          }
        }

        this.fileList = this.fileList.concat(this.uploadList);
        this.uploadList = [];
        this.number = 0;
        this.$emit("fileList", this.fileList);
        this.$modal.closeLoading();
      }
    },
    // 获取文件名称
    /* getFileName(name) {
      if (name.lastIndexOf("/") > -1) {
        return name.slice(name.lastIndexOf("/") + 1);
      } else {
        return "";
      }
    }, */
    getFileType(name) {
      if (name.lastIndexOf(".") > -1) {
        return name.slice(name.lastIndexOf(".") + 1);
      } else {
        return "";
      }
    },
    // 对象转成指定字符串分隔
    listToString(list, separator) {
      let strs = "";
      separator = separator || ",";
      for (let i in list) {
        strs += list[i].url + separator;
      }
      return strs != '' ? strs.substr(0, strs.length - 1) : '';
    }
  }
};
</script>

<style scoped lang="scss">
.course-upload-file {
  .upload-file-uploader {
    margin-bottom: 5px;
    text-align: center;
  }

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
</style>

