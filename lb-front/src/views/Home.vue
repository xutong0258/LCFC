<template>
  <div class="container">
    <el-row class="head-class">
      <img src="@/assets/home-icon.png" class="hone-icon">首页
    </el-row>
    <el-row class="head-top">
      Issue数据概览
      <el-button plain @click="dialogVisible = true">
        上传Issue数据概览
      </el-button>


    </el-row>
    <el-row :gutter="24">
      <el-col :span="6">
        <el-card shadow="hover" class="top-card">
          <div class="top-head">
            <div class="top-title">Issue总数</div>
            <img src="@/assets/top-total.png">
          </div>
          <div class="top-num">{{ statData.total_count || 0 }}</div>
          <div class="top-unit">条</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="top-card">
          <div class="top-head">
            <div class="top-title">本月新增Issue</div>
            <img src="@/assets/top-new.png">
          </div>
          <div class="top-num">{{ statData.total_count || 0 }}</div>
          <div class="top-unit">条</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="top-card">
          <div class="top-head">
            <div class="top-title">待处理Issue</div>
            <img src="@/assets/top-waiting.png">
          </div>
          <div class="top-num" style="color: #FAAD14">{{ statData.pending_count || 0 }}</div>
          <div class="top-unit">条</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="top-card">
          <div class="top-head">
            <div class="top-title">Issue分析</div>
            <img src="@/assets/top-assay.png">
          </div>
          <div class="top-num">{{ statData.diagnosis_count || 0 }}</div>
          <div class="top-unit">次</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px;margin-bottom:16px">
      <el-col :span="18">
        <div class="span-left"><img src="@/assets/analysis-icon.png">
          <div>软件Issue诊断</div>
        </div>
      </el-col>
      <el-col :span="6">

        <div class="span-right"><span style="font-size: 14px">查看更多</span>
          <img src="@/assets/right-icon.png">
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="24">
      <el-col :span="4">
        <el-card shadow="hover" class="mid-card">
          <img src="@/assets/windbg.png">
          <div class="mid-title">WinDBG</div>
          <div class="mid-desc">Windows调试工具</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="mid-card">
          <img src="@/assets/kd.png">
          <div class="mid-title">KD</div>
          <div class="mid-desc">内核调试器</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="mid-card">
          <img src="@/assets/xnjsq.png">
          <div class="mid-title">性能监视器</div>
          <div class="mid-desc">系统性能分析</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="mid-card">
          <img src="@/assets/sjckq.png">
          <div class="mid-title">事件查看器</div>
          <div class="mid-desc">系统日志分析</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="mid-card">
          <img src="@/assets/wljc.png">
          <div class="mid-title">网络监测</div>
          <div class="mid-desc">网络连接诊断</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="mid-card">
          <img src="@/assets/gzzd.png">
          <div class="mid-title">故障诊断</div>
          <div class="mid-desc">硬件故障检测</div>
        </el-card>
      </el-col>

    </el-row>
    <el-row :gutter="24" style="margin-top: 16px">
      <el-col :span="24">
        <el-card shadow="hover" class="bottom-card">
          <div class="span-left"><img src="@/assets/issue-waiting.png">
            <div>待处理Issue</div>
          </div>
          <el-table
            :data="issueList"
            style="width: 100%" class="header-table-th">
            <el-table-column
              prop="issueNumber"
              label="Issue ID"
            >
            </el-table-column>
            <el-table-column
              prop="title"
              label="标题"
            >
            </el-table-column>
            <el-table-column
              prop="priority"
              label="优先级">
              <template v-slot="scope">
                <span v-if="scope.row.priority=='high'" class="status-higth">高</span>
                <span v-if="scope.row.priority=='medium'" class="status-waiting">中</span>
                <span v-if="scope.row.priority=='low'" class="status-finish">低</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="status"
              label="状态">
              <template v-slot="scope">
                <span v-if="scope.row.status=='pending'" class="status-waiting">待诊断</span>
                <span v-if="scope.row.status=='diagnosing'" class="status-diag">诊断中</span>
                <span v-if="scope.row.status=='completed'" class="status-finish">已完成</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="createTime"
              label="提交时间" >
              <template v-slot="scope">
                {{ dayjs(scope.row.createTime).format('YYYY-MM-DD HH:mm:ss') }}
              </template>
            </el-table-column>
            <el-table-column
              prop="option"
              label="操作">
              <template v-slot="scope">
                <el-button size="small" type="text" @click="toDetail(scope.row)">查看详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    <UploadData v-model="dialogVisible"></UploadData>
  </div>
</template>

<script>
import { useGet } from "@/utils/request.js";
import { ElMessage } from "element-plus";
import UploadData from './dataView/uploadData.vue';
import dayjs from 'dayjs'

export default {
  components: { UploadData },

  data() {
    return {
      dialogVisible: false,
      statData: {},
      issueList: [],
      total:0
    }
  },
  created() {
    this.getStat()
    this.getIssueList()
  },
  methods: {
    dayjs,
    getStat() {
      useGet('/system/issue/statistics', {}).then((res) => {
        console.log(res)
        const { data, success, message } = res
        if (success) {
          this.statData = data || {}
        } else {
          ElMessage.error(message || '请求失败')
        }
      })
    },
    toDetail(row) {
      this.$router.push({
        path: '/detail',
        query: {
          id: row.issueId,
        }
      });

    },//获取列表
    getIssueList() {
      const payload = {}
      payload.pageNum = 1
      payload.pageSize = 10
      payload.status='pending'
      useGet('/system/issue/list', payload).then((res) => {
        const { data, success, message } = res
        if (success) {
          this.issueList = data.rows ||[]
          this.total = data.total
        } else {
          ElMessage.error(message || '请求失败')
        }
      })
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

.hone-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;

}

.head-class {
  font-size: 14px;
  color: #666666;
  display: flex;
  align-items: center;
}

.head-top {
  font-family: 'AlibabaPuHuiTi';
  font-size: 20px;
  font-weight: normal;
  line-height: 30px;
  display: flex;
  align-items: center;
  color: #333333;
  margin-top: 18px;
  margin-bottom: 16px;
}

.top-card {
  border-radius: 8px;
  border: 0px !important;

  .top-head {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .top-title {
      font-family: 'AlibabaPuHuiTi';
      font-size: 14px;
      font-weight: normal;
      line-height: 21px;
      display: flex;
      align-items: center;
      color: #666666;
    }

    img {
      width: 40px;
      height: 40px;
    }
  }

  .top-num {
    font-family: AlibabaPuHuiTi;
    font-size: 24px;
    font-weight: normal;
    line-height: 36px;
    display: flex;
    align-items: center;
    color: #1677FF;
  }

  .top-unit {
    font-family: 'AlibabaPuHuiTi';
    font-size: 14px;
    font-weight: normal;
    line-height: 21px;
    display: flex;
    align-items: center;
    color: #666666;
  }


}

.span-left {
  display: flex;
  align-items: center;
  flex-direction: row;
  font-family: 'AlibabaPuHuiTi';
  font-size: 18px;
  font-weight: normal;
  line-height: 27px;
  display: flex;

  color: #333333;

  img {
    width: 20px;
    height: 20px;
    margin-right: 4px;
  }
}

.span-right {
  display: flex;
  align-items: center;
  flex-direction: row;
  font-family: 'AlibabaPuHuiTi';
  font-weight: normal;
  line-height: 27px;
  display: flex;
  color: #1677FF;
  justify-content: right;

  img {
    width: 12px;
    height: 12px;
    margin-left: 7px;
  }
}

.mid-card {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  border-radius: 8px;
  border: 1px solid #EAEAEA;

  img {
    width: 48px;
    height: 48px;
    margin-bottom: 7.5px;
  }

  .mid-title {
    font-family: 'AlibabaPuHuiTi';
    font-size: 15px;
    font-weight: normal;
    line-height: 22.5px;
    color: #333333;
  }

  .mid-desc {
    font-family: 'AlibabaPuHuiTi';
    font-size: 12px;
    font-weight: normal;
    line-height: 18px;
    color: #666666;
  }
}

::v-deep .mid-card .el-card__body {
  padding: 13px !important;
}

.bottom-card {
  border-radius: 8px;

  .span-left {
    font-family: 'AlibabaPuHuiTi';
    font-size: 16px;
    font-weight: normal;
    line-height: 24px;
    display: flex;
    align-items: center;
    color: #333333;
    padding-bottom: 16px;
  }
}

::v-deep .header-table-th .el-table__header th {
  background-color: #F5F7FA;
}

.status-finish {
  font-family: 'AlibabaPuHuiTi';
  font-size: 12px;
  font-weight: normal;
  line-height: 18px;
  display: inline-flex;
  align-items: center;
  letter-spacing: 0px;
  color: #52C41A;
  padding: 2px 8px;
  background: #F6FFED;
  border-radius: 4px;
  min-width: 28px;
  min-width: 14px;
  white-space: nowrap;
}

.status-waiting {
  font-family: 'AlibabaPuHuiTi';
  font-size: 12px;
  font-weight: normal;
  line-height: 18px;
  align-items: center;
  color: #FAAD14;
  padding: 2px 8px;
  background-color: #FFF7E6;
  border-radius: 4px;
  min-width: 14px;
  display: inline-flex;
}

.status-higth {
  font-family: 'AlibabaPuHuiTi';
  font-size: 12px;
  font-weight: normal;
  line-height: 18px;
  display: inline-flex;
  align-items: center;
  letter-spacing: 0px;
  color: #FF4D4F;
  padding: 2px 8px;
  background: #FFF2F0;
  border-radius: 4px;
  min-width: 14px;

}

.status-diag {
  font-family: 'AlibabaPuHuiTi';
  font-size: 12px;
  font-weight: normal;
  line-height: 18px;
  display: inline-flex;
  align-items: center;
  letter-spacing: 0px;
  color: #1677FF;
  padding: 2px 8px;
  background: #E6F4FF;
  border-radius: 4px;
  min-width: 14px;

}
</style>
