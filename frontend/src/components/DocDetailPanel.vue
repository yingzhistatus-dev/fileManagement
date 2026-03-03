<template>
  <div class="card" v-if="currentDoc && currentDoc.detailData">
    <div class="detail-header">
      <h3>文档详情</h3>
      <button class="table-btn" @click="$emit('close')">关闭</button>
    </div>

    <div class="detail-grid">
      <div class="detail-item">
        <span class="detail-label">文件名称</span>
        <span class="detail-value">{{ currentDoc.detailData.fileName || currentDoc.fileName }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">上传时间</span>
        <span class="detail-value">{{ currentDoc.detailData.uploadTime || '-' }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">分段数量</span>
        <span class="detail-value">{{ currentDoc.detailData.segmentTotalNum || 0 }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">分段方式</span>
        <span class="detail-value">{{ formatSegmentMode(currentDoc.detailData.segmentMethod) }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">最大长度</span>
        <span class="detail-value">{{ currentDoc.detailData.maxSegmentSize || '-' }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">解析方式</span>
        <span class="detail-value">{{ formatAnalyzerText(currentDoc.detailData.docAnalyzerText) }}</span>
      </div>
    </div>

    <div class="segment-list" v-if="(currentDoc.detailData.contentList || []).length">
      <div
        class="segment-card"
        v-for="seg in currentDoc.detailData.contentList"
        :key="seg.contentId"
      >
        <div class="segment-title">分段 {{ seg.contentNum }}</div>
        <div class="segment-content">{{ seg.content }}</div>
      </div>
    </div>

    <div class="empty-box" v-else>
      当前文档暂无分段内容
    </div>
  </div>
</template>

<script>
export default {
  name: 'DocDetailPanel',
  props: {
    currentDoc: Object
  },
  emits: ['close'],
  methods: {
    formatSegmentMode(value) {
      if (value === 0 || value === '0') return '通用分段'
      if (value === 1 || value === '1') return '父子分段'
      return value || '通用分段'
    },
    formatAnalyzerText(value) {
      if (Array.isArray(value)) return value.length ? value.join('、') : '-'
      return value || '-'
    }
  }
}
</script>

<style scoped src="../assets/styles/common.css"></style>
<style scoped src="../assets/styles/doc-detail.css"></style>