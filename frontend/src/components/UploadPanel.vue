<template>
  <div class="card upload-panel">
    <h2>文件解析 Demo</h2>
    <p class="desc">该页面用于演示文件上传、参数设置、后端解析以及结果展示流程。</p>

    <input
      ref="fileInput"
      type="file"
      class="hidden-file-input"
      @change="onFileChange"
    />

    <div class="form-section actions">
      <button class="btn" :disabled="uploading || parsing" @click="chooseFile">
        {{ selectedFile ? '重新选择文件' : '上传文件' }}
      </button>

      <button
        class="btn btn-success"
        :disabled="!selectedFile || uploading || parsing"
        @click="$emit('next-step')"
      >
        下一步：参数设置
      </button>

      <button
        class="btn btn-warning"
        :disabled="summarizing || !canGenerateSummary"
        @click="$emit('generate-summary')"
      >
        {{ summarizing ? '生成中...' : '生成摘要' }}
      </button>

      <button
        class="btn btn-danger"
        :disabled="deletingBatch || !selectedCount"
        @click="$emit('batch-delete')"
      >
        {{ deletingBatch ? '删除中...' : '批量删除' }}
      </button>

      <button class="btn btn-default" :disabled="loadingDocs" @click="$emit('refresh')">
        {{ loadingDocs ? '刷新中...' : '刷新文档列表' }}
      </button>
    </div>

    <div class="toolbar-tip">
      <span>已选择 {{ selectedCount }} 项</span>
      <span class="tip-inline" v-if="selectedCount > 1">
        当前版本一次只支持选择 1 个文档生成摘要
      </span>
    </div>

    <div class="form-section info-box" v-if="selectedFile">
      <p><strong>当前文件：</strong>{{ selectedFile.name }}</p>
    </div>

    <div class="form-section" v-if="message">
      <div class="message">{{ message }}</div>
    </div>

    <p class="tip" v-if="parseMode === 'wanwu'">
      当前文件已完成万悟解析任务接入，摘要功能将基于“查看详情”返回的分段内容生成。
    </p>
  </div>
</template>

<script>
export default {
  name: 'UploadPanel',
  props: {
    selectedFile: Object,
    message: String,
    uploading: Boolean,
    parsing: Boolean,
    summarizing: Boolean,
    deletingBatch: Boolean,
    loadingDocs: Boolean,
    selectedCount: {
      type: Number,
      default: 0
    },
    canGenerateSummary: Boolean,
    parseMode: String
  },
  emits: ['file-change', 'next-step', 'generate-summary', 'batch-delete', 'refresh'],
  methods: {
    chooseFile() {
      this.$refs.fileInput && this.$refs.fileInput.click()
    },
    onFileChange(event) {
      this.$emit('file-change', event)
    }
  }
}
</script>

<style scoped src="../assets/styles/common.css"></style>
<style scoped src="../assets/styles/parse-demo.css"></style>

<style scoped>
.hidden-file-input {
  display: none;
}
</style>