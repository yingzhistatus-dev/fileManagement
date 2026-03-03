<template>
  <div class="report-page">
    <div class="card">
      <div class="page-header">
        <div>
          <h2>社区报告</h2>
          <p class="desc">展示当前知识库的社区报告生成状态与报告内容。</p>
        </div>

        <div class="actions">
          <button class="btn" :disabled="loading" @click="loadReports">
            {{ loading ? '刷新中...' : '刷新数据' }}
          </button>
          <button class="btn btn-success" :disabled="generating" @click="handleGenerate">
            {{ generating ? '生成中...' : (reportMeta?.generateLabel || '重新生成') }}
          </button>
          <button class="btn btn-default" @click="handleAddReport">
            新增社区报告
          </button>
        </div>
      </div>

      <div class="message" v-if="message">
        {{ message }}
      </div>

      <div class="meta-table" v-if="reportMeta">
        <div class="meta-row">
          <div class="meta-label">名称</div>
          <div class="meta-value">社区报告</div>
          <div class="meta-label">社区报告数量</div>
          <div class="meta-value">{{ reportMeta.total ?? 0 }}</div>
          <div class="meta-label">生成时间</div>
          <div class="meta-value">{{ formatTime(reportMeta.createdAt) }}</div>
        </div>
        <div class="meta-row">
          <div class="meta-label">状态</div>
          <div class="meta-value">{{ formatStatus(reportMeta.status) }}</div>
          <div class="meta-label">批量新增状态</div>
          <div class="meta-value">{{ formatImportStatus(reportMeta.lastImportStatus) }}</div>
          <div class="meta-label"></div>
          <div class="meta-value"></div>
        </div>
      </div>

      <div class="empty-card" v-else-if="!loading">
        暂未获取到社区报告元数据
      </div>
    </div>

    <div class="card" v-if="reports.length">
      <div class="report-grid">
        <div
          class="report-card"
          v-for="item in reports"
          :key="item.contentId"
          :class="{ active: currentReport && currentReport.contentId === item.contentId }"
          @click="currentReport = item"
        >
          <div class="report-title">{{ item.title }}</div>
          <div class="report-preview">{{ getPreview(item.content) }}</div>
        </div>
      </div>

      <div class="pager">
        <span>共 {{ reportMeta?.total || 0 }} 条</span>
        <button class="pager-btn" :disabled="pageNo <= 1 || loading" @click="changePage(pageNo - 1)">
          上一页
        </button>
        <span>{{ pageNo }}</span>
        <button
          class="pager-btn"
          :disabled="pageNo >= totalPages || loading"
          @click="changePage(pageNo + 1)"
        >
          下一页
        </button>
      </div>
    </div>

    <div class="card" v-else-if="!loading">
      <div class="empty-card">当前暂无社区报告</div>
    </div>

    <div class="card" v-if="currentReport">
      <div class="detail-header">
        <h3>{{ currentReport.title }}</h3>
      </div>
      <div class="report-content">{{ currentReport.content }}</div>
    </div>
  </div>
</template>

<script>
import { getReportList, generateReport } from '../api/report'

export default {
  name: 'ReportDemo',
  data() {
    return {
      loading: false,
      generating: false,
      message: '',
      reportMeta: null,
      reports: [],
      currentReport: null,
      pageNo: 1,
      pageSize: 8
    }
  },
  computed: {
    totalPages() {
      const total = this.reportMeta?.total || 0
      return Math.max(1, Math.ceil(total / this.pageSize))
    }
  },
  mounted() {
    this.loadReports()
  },
  methods: {
    async loadReports() {
      try {
        this.loading = true
        this.message = '正在加载社区报告...'

        const res = await getReportList({
          pageNo: this.pageNo,
          pageSize: this.pageSize
        })

        const data = res?.data || {}
        this.reportMeta = data
        this.reports = Array.isArray(data.list) ? data.list : []
        this.currentReport = this.reports[0] || null
        this.message = res?.message || '获取社区报告列表成功'
      } catch (error) {
        this.reportMeta = null
        this.reports = []
        this.currentReport = null
        this.message = `获取社区报告列表失败：${error.message}`
      } finally {
        this.loading = false
      }
    },

    async handleGenerate() {
      try {
        this.generating = true
        this.message = '正在提交社区报告生成任务...'

        const res = await generateReport()
        this.message = res?.message || '已提交社区报告生成任务'

        await this.loadReports()
      } catch (error) {
        this.message = `生成社区报告失败：${error.message}`
      } finally {
        this.generating = false
      }
    },

    handleAddReport() {
      this.message = '“新增社区报告”接口暂未接入，等你抓到接口后我再帮你补上。'
    },

    changePage(page) {
      this.pageNo = page
      this.loadReports()
    },

    getPreview(content) {
      return (content || '').replace(/\n/g, ' ').slice(0, 180)
    },

    formatStatus(status) {
      if (status === 2) return '已生成'
      if (status === 1) return '生成中'
      if (status === 3) return '生成失败'
      return String(status ?? '-')
    },

    formatImportStatus(status) {
      if (status === -1) return '-'
      if (status === 0) return '待处理'
      if (status === 1) return '导入中'
      if (status === 2) return '完成'
      if (status === 3) return '失败'
      return String(status ?? '-')
    },

    formatTime(ts) {
      if (!ts || ts === '-') return '-'
      const num = Number(ts)
      if (!Number.isFinite(num)) return ts
      const date = new Date(num)
      const pad = n => String(n).padStart(2, '0')
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
    }
  }
}
</script>

<style scoped>
.report-page {
  max-width: 1400px;
  margin: 0 auto;
}

.card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  margin-bottom: 20px;
}

.page-header,
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.desc {
  color: #666;
  margin: 8px 0 0;
}

.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn {
  border: none;
  background: #1f6feb;
  color: #fff;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
}

.btn:disabled {
  background: #9bbcf3;
  cursor: not-allowed;
}

.btn-success {
  background: #16a34a;
}

.btn-default {
  background: #64748b;
}

.message {
  padding: 12px 14px;
  background: #eef4ff;
  color: #1f3b75;
  border-radius: 8px;
  margin-bottom: 16px;
}

.meta-table {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.meta-row {
  display: grid;
  grid-template-columns: 120px 1fr 160px 1fr 140px 1fr;
}

.meta-row + .meta-row {
  border-top: 1px solid #e5e7eb;
}

.meta-label,
.meta-value {
  padding: 16px 14px;
  border-right: 1px solid #e5e7eb;
}

.meta-label {
  background: #fafafa;
  color: #64748b;
}

.meta-value:last-child,
.meta-label:last-child {
  border-right: none;
}

.report-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.report-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  background: #fff;
  min-height: 240px;
}

.report-card.active {
  border-color: #1f6feb;
  box-shadow: 0 0 0 2px rgba(31, 111, 235, 0.08);
}

.report-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 14px;
  line-height: 1.5;
}

.report-preview {
  color: #374151;
  line-height: 1.8;
  word-break: break-word;
}

.report-content {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.9;
  color: #1f2937;
}

.pager {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.pager-btn {
  border: 1px solid #d1d5db;
  background: #fff;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

.pager-btn:disabled {
  color: #94a3b8;
  cursor: not-allowed;
}

.empty-card {
  color: #64748b;
}

@media (max-width: 1200px) {
  .report-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .meta-row {
    grid-template-columns: 120px 1fr 120px 1fr;
  }

  .meta-row .meta-label:nth-child(5),
  .meta-row .meta-value:nth-child(6) {
    display: none;
  }
}

@media (max-width: 768px) {
  .page-header,
  .detail-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .report-grid {
    grid-template-columns: 1fr;
  }

  .meta-row {
    grid-template-columns: 100px 1fr;
  }

  .meta-row .meta-label:nth-child(n+3),
  .meta-row .meta-value:nth-child(n+4) {
    display: none;
  }
}
</style>