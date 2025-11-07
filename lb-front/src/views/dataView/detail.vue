<template xmlns="http://www.w3.org/1999/html">
  <div class="container">
    <el-row class="head-class">
      <img src="../../assets/detail-icon.png" class="hone-icon">首页 <span class="home-right-icon"> > </span>Issue数据概览
      <span class="home-right-icon"> > </span>Issue详情
    </el-row>
    <el-row :gutter="24">
      <el-col>
        <el-card class="top-card">
          <div class="card-top">
            <div class="top-left">
              <div class="left-id">{{ issueInfo.issueNumber ||'-' }}</div>
              <div class="left-time"><img src="../../assets/time-icon.png" class="time-icon"/>提交时间：<span v-if="issueInfo.createTime">{{dayjs(issueInfo.createTime).format('YYYY-MM-DD HH:mm:ss') }}</span><span v-else>-</span>
              </div>
            </div>
            <div class="top-right">
              <span class="right-level">
                <span v-if="issueInfo.priority=='high'">高</span>
                <span v-if="issueInfo.priority=='medium'">中</span>
                <span v-if=" issueInfo.priority=='low'">低</span>优先级</span>
              <span class="right-status"><span v-if="issueInfo.status=='pending'" class="status-waiting">待诊断</span>
                <span v-if="issueInfo.status=='diagnosing'" class="status-diag">诊断中</span>
                <span v-if="issueInfo.status=='completed'" class="status-finish">已完成</span></span>
            </div>
          </div>
          <div class="mid-title">{{ issueInfo.title }}</div>
          <div class="btm-card">
            <div><img src="../../assets/person-icon.png" class="time-icon"/>提交人：{{ issueInfo.createBy ||'-'}}</div>
            <div><img src="../../assets/person-icon.png" class="time-icon"/>责任人：{{ issueInfo.updateBy ||'-'}}</div>
            <div><img src="../../assets/tool-icon.png" class="time-icon"/>诊断工具：WinDBG</div>
            <div><img src="../../assets/time-icon.png" class="time-icon"/>更新时间：<span v-if="issueInfo.createTime">{{dayjs(issueInfo.updateTime).format('YYYY-MM-DD HH:mm:ss') }}</span><span v-else>-</span></div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="24">
      <el-col>
        <el-card class="ques-card">
          <div class="top-title"><img src="../../assets/ask-icon.png" class="title-icon-img"/>问题描述
          </div>
          <div class="ques-content">
            {{ issueInfo.description }}
<!--            <div>操作系统版本：Windows 11 专业版 21H2</div>-->
<!--            <div>问题现象：系统在启动某软件后约10分钟出现蓝屏，错误代码为：SYSTEM_SERVICE_EXCEPTION (0x0000003b)</div>-->
<!--            <div>问题复现步骤：</div>-->
<!--            <div style="padding-left: 24px">启动计算机，进入Windows系统<br>-->
<!--              打开目标应用程序XYZ软件<br>-->
<!--              进行正常操作约10分钟<br>-->
<!--              系统出现蓝屏崩溃<br>-->
<!--            </div>-->
<!--            <div>问题频率：100%可复现</div>-->
<!--            <div>附加信息：同样的软件在Windows 10系统上运行正常，未发现类似问题。系统已更新至最新补丁。</div>-->
          </div>
        </el-card>
      </el-col>

    </el-row>

    <el-row :gutter="24">
      <el-col>
        <el-card class="sys-card">
          <div class="top-title"><img src="../../assets/sys-icon.png" class="title-icon-img"/>系统环境
          </div>
          <el-row :gutter="24">
            <el-col :span="12">
              <div>CPU：{{ systemEnv.cpuInfo||'-' }}</div>
              <div>显卡：{{ systemEnv.gpuInfo||'-' }}</div>
              <div>驱动版本：{{ systemEnv.gpuDriverVersion||'-' }}</div>
            </el-col>
            <el-col :span="12">
              <div>内存：{{ systemEnv.memoryInfo ||'-'}}</div>
              <div>操作系统：{{ systemEnv.osInfo ||'-'}}</div>
              <div>BIOS版本：{{ systemEnv.biosVersion ||'-'}}</div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24">
      <el-col :span="24">
        <el-card class="sys-card">
          <div class="top-title"><img src="../../assets/his-icon.png" class="title-icon-img"/>诊断记录
          </div>
          <div style="display: flex;flex-direction: column;gap: 24px">
            <div class="card-top" v-for="(item,index) in diagnosisLogs">
              <img src="../../assets/step-icon.png" class="step-icon"/>
              <div>
                <div class="sys-title">{{ item.stepName }}<span class="sys-time">{{ item.operateTime }}</span><span
                  class="sys-person">操作人：{{ item.operator }}</span></div>
                <div class="sya.desc">{{ item.methodDescription }}</div>
              </div>
            </div>
            <el-empty v-if="diagnosisLogs.length==0 "></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24">
      <el-col>
        <el-card class="ques-card">
          <div class="top-title"><img src="../../assets/fn-icon.png" class="title-icon-img"/>解决方案
          </div>
          <div class="ques-content">
            {{ issueInfo.solution ||'-'}}
<!--            <div>建议更新NVIDIA驱动至最新版本（512.15或更高），此版本已修复与Windows 11系统的兼容性问题。</div>-->
<!--            <div>具体操作步骤：</div>-->
<!--            <div style="padding-left: 24px">访问NVIDIA官方网站下载最新驱动程序<br>-->
<!--              完全卸载当前版本的驱动程序<br>-->
<!--              重启系统<br>-->
<!--              安装新版驱动程序<br>-->
<!--              重启系统并测试<br>-->
<!--            </div>-->
          </div>
        </el-card>
      </el-col>

    </el-row>
    <el-row :gutter="24">
      <el-col>
        <el-card class="ques-card">
          <div class="top-title"><img src="../../assets/sell-icon.png" class="title-icon-img"/>相关Issue推荐
          </div>
          <div class="issue-content">
            <div class="issue-cell">
              <div class="issue-left"><span>ISU-2023-1498</span><span style="padding-left: 15px;color: #333333">Windows 11系统驱动兼容性问题</span>
              </div>
              <div class="issue-right">
                <div class="right-level">高</div>
                <div class="right-status">已完成</div>
              </div>
            </div>
            <div class="issue-cell">
              <div class="issue-left"><span>ISU-2023-1498</span><span style="padding-left: 15px;color: #333333">Windows 11系统驱动兼容性问题</span>
              </div>
              <div class="issue-right">
                <div class="right-level">高</div>
                <div class="right-status">已完成</div>
              </div>
            </div>
            <div class="issue-cell">
              <div class="issue-left"><span>ISU-2023-1498</span><span style="padding-left: 15px;color: #333333">Windows 11系统驱动兼容性问题</span>
              </div>
              <div class="issue-right">
                <div class="right-level">高</div>
                <div class="right-status">已完成</div>
              </div>
            </div>

          </div>
        </el-card>
      </el-col>

    </el-row>
    <el-row :gutter="24">
      <el-col :span="24" style="display:flex;justify-content: right">
        <el-button type="primary" style="margin-top: 24px" @click="toHome">返回列表</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { useGet } from "@/utils/request.js";
import { ElMessage } from "element-plus";
import dayjs from 'dayjs'

export default {
  props: ['id'],
  data() {
    return {
      issueInfo: {},
      systemEnv: {},
      diagnosisLogs: [],
      attachments: [],
      tags: []
    }
  },

  created() {
    this.getIssueDetail()
  },
  methods: {
    dayjs,
    getIssueDetail() {
      useGet('/system/issue/' + this.id,{}).then((res) => {
        const { data, success, message } = res
        if (success) {
          //Issue基本信息
          this.issueInfo = data.issue_info
          //系统环境信息
          this.systemEnv = data.issue_info
          //诊断记录列表
          this.diagnosisLogs = data.diagnosis_logs
          //附件列表
          this.attachments = data.attachments
          //标签列表
          this.tags = data.tags

        } else {
          ElMessage.error(message || '请求失败')
        }
      })
    },toHome(){
      this.$router.push({
        path: '/',
      });
    }

  }
}
</script>

<style scoped>
.container {
  height: 100%;
  background-color: #F5F7FA;
  padding: 20px;
  box-sizing: border-box;
}

.head-class {
  font-size: 14px;
  color: #666666;
  display: flex;
  align-items: center;
}

.hone-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;

}

.home-right-icon {
  padding: 0px 8px;
}

.top-card {
  margin-top: 24px;
  border-radius: 8px !important;

  .top-left {
    display: flex;
    align-items: center;

    .left-id, .left-time {
      font-family: 'AlibabaPuHuiTi';
      font-size: 16px;
      font-weight: normal;
      line-height: 24px;
      display: flex;
      align-items: center;
      color: #1677FF;
      padding-right: 19px;
    }

    .time-icon {
      width: 16px;
      height: 16px;
      margin-right: 4px;
    }

    .left-time {
      color: #6B7280;
    }
  }

  .top-right {
    display: flex;
    flex-direction: row;
    gap: 12px;

    .right-level {
      font-family: 'AlibabaPuHuiTi';
      font-size: 12px;
      font-weight: normal;
      line-height: 16px;
      display: flex;
      align-items: center;
      color: #FF4D4F;
      background-color: #FFF2F0;
      padding: 4px 12px;
      border-radius: 4px;
    }

    .right-status {
      font-family: 'AlibabaPuHuiTi';
      font-size: 12px;
      font-weight: normal;
      line-height: 16px;
      display: flex;
      align-items: center;
      letter-spacing: 0px;
      color: #FAAD14;
      background-color: #FFF7E6;
      padding: 4px 12px;
      border-radius: 4px;

    }
  }

  .mid-title {
    font-family: AlibabaPuHuiTi;
    font-size: 20px;
    font-weight: normal;
    line-height: 28px;
    display: flex;
    align-items: center;
    color: #333333;
    padding: 16px 0px 24px 0px;
  }

  .btm-card {
    font-family: AlibabaPuHuiTi;
    font-size: 16px;
    font-weight: normal;
    line-height: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    letter-spacing: 0px;
    color: #4B5563;

    img {
      width: 16px;
      height: 16px;
      margin-right: 4px;
    }
  }
}

.top-card .card-top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

::v-deep .top-card .el-card__body {
  padding: 24px !important;
}

.top-card {
  border-radius: 8px !important;
}

.ques-card {
  margin-top: 24px;

  .top-title {
    font-family: 'AlibabaPuHuiTi';
    font-size: 18px;
    font-weight: normal;
    line-height: 28px;
    display: flex;
    align-items: center;
    color: #333333;
  }

  .ques-content {
    font-family: 'AlibabaPuHuiTi';
    font-size: 16px;
    font-weight: normal;
    line-height: 24px;
    display: flex;
    flex-direction: column;
    color: #333333;
    padding-top: 16px;
    text-align: left;
    gap: 12px;
  }
}

.title-icon-img {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}

.sys-card {
  margin-top: 24px;

  .top-title {
    font-family: 'AlibabaPuHuiTi';
    font-size: 18px;
    font-weight: normal;
    line-height: 28px;
    display: flex;
    align-items: center;
    color: #333333;
    padding-bottom: 17px;
  }

  .card-top {
    font-family: AlibabaPuHuiTi;
    font-size: 16px;
    font-weight: normal;
    line-height: 24px;
    letter-spacing: 0px;
    color: #333333;
    display: flex;
    align-items: baseline;

  }

  .step-icon {
    width: 16px;
    height: 16px;
    margin-right: 16px;
  }

  .sys-time, .sys-person {
    font-family: AlibabaPuHuiTi;
    font-size: 14px;
    font-weight: normal;
    line-height: 20px;
    display: flex;
    align-items: center;
    color: #6B7280;
  }

  .sys-title {
    display: flex;
    gap: 12px;
  }
}

.issue-content {
  margin-top: 16px;
}

.issue-cell {
  min-height: 49px;
  display: flex;
  justify-content: space-between;
  flex-direction: row;
  align-items: center;
  border-bottom: 1px solid #F3F4F6;

  .issue-left {
    font-family: AlibabaPuHuiTi;
    font-size: 16px;
    font-weight: normal;
    line-height: 24px;
    display: flex;
    align-items: center;
    letter-spacing: 0px;

    color: #1677FF;
  }

  .issue-right {
    display: flex;
    gap: 24px;

    .right-level {
      font-family: 'AlibabaPuHuiTi';
      font-size: 12px;
      font-weight: normal;
      line-height: 16px;
      display: flex;
      align-items: center;
      color: #FF4D4F;
      background-color: #FFF2F0;
      padding: 4px 12px;
      border-radius: 4px;
    }

    .right-status {
      font-family: 'AlibabaPuHuiTi';
      font-size: 12px;
      font-weight: normal;
      line-height: 16px;
      display: flex;
      align-items: center;
      letter-spacing: 0px;
      color: #FAAD14;
      background-color: #FFF7E6;
      padding: 4px 12px;
      border-radius: 4px;
    }
  }
}
</style>
