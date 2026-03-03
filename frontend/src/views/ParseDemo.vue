<template>
  <div class="page">
    <UploadPanel
      :selected-file="selectedFile"
      :message="message"
      :uploading="uploading"
      :parsing="parsing"
      :summarizing="summarizing"
      :deleting-batch="deletingBatch"
      :loading-docs="loadingDocs"
      :selected-count="selectedDocIds.length"
      :can-generate-summary="canGenerateSummary"
      :parse-mode="parseResult?.mode"
      @file-change="handleFileChange"
      @next-step="openUploadConfigDialog"
      @generate-summary="handleGenerateSelectedSummary"
      @batch-delete="handleBatchDelete"
      @refresh="loadDocsList"
    />

    <SummaryPanel :summary-text="summaryText" />

    <DocTable
      :docs-list="docsList"
      :selected-doc-ids="selectedDocIds"
      :loading-docs="loadingDocs"
      :is-all-selected="isAllSelected"
      :is-indeterminate="isIndeterminate"
      @toggle-select-all="toggleSelectAll"
      @toggle-select-doc="toggleSelectDoc"
      @delete-doc="handleDelete"
      @segment-doc="handleSegment"
      @view-doc="handleView"
    />

    <DocDetailPanel
      :current-doc="currentDoc"
      @close="currentDoc = null"
    />

    <ConfigDialog
      :visible="showConfigDialog"
      :saving="savingConfig"
      :title="configDialogMode === 'upload' ? '参数设置' : '分段设置'"
      :config="configForm"
      :splitter-text="splitterText"
      :sub-splitter-text="subSplitterText"
      @close="closeConfigDialog"
      @submit="submitConfigDialog"
    />
  </div>
</template>

<script>
import UploadPanel from '../components/UploadPanel.vue'
import SummaryPanel from '../components/SummaryPanel.vue'
import DocTable from '../components/DocTable.vue'
import DocDetailPanel from '../components/DocDetailPanel.vue'
import ConfigDialog from '../components/ConfigDialog.vue'

import { uploadFile } from '../api/upload'
import { parseFile } from '../api/parse'
import { generateSummary } from '../api/summary'
import {
  getDocsList,
  deleteDocs,
  getDocDetail,
  getDocConfig,
  updateDocConfig
} from '../api/docs'

export default {
  name: 'ParseDemo',
  components: {
    UploadPanel,
    SummaryPanel,
    DocTable,
    DocDetailPanel,
    ConfigDialog
  },
  data() {
    return {
      selectedFile: null,
      fileId: '',
      parsedText: '',
      summaryText: '',
      message: '',
      parseResult: null,
      uploading: false,
      parsing: false,
      summarizing: false,
      deletingBatch: false,
      loadingDocs: false,
      savingConfig: false,
      docsList: [],
      currentDoc: null,
      selectedDocIds: [],

      showConfigDialog: false,
      configDialogMode: 'upload',
      currentConfigDoc: null,
      splitterText: '\\n\\n',
      subSplitterText: '\\n',
      configForm: {
        docImportType: 0,
        docSegment: {
          segmentMethod: '0',
          segmentType: '0',
          splitter: ['\\n\\n'],
          maxSplitter: 1024,
          overlap: 0.2,
          subSplitter: ['\\n'],
          subMaxSplitter: 4000
        },
        docAnalyzer: ['text'],
        parserModelId: '',
        docPreprocess: ['replaceSymbols'],
        docMetaData: []
      }
    }
  },
  computed: {
    isAllSelected() {
      return this.docsList.length > 0 && this.selectedDocIds.length === this.docsList.length
    },
    isIndeterminate() {
      return this.selectedDocIds.length > 0 && this.selectedDocIds.length < this.docsList.length
    },
    canGenerateSummary() {
      return this.selectedDocIds.length === 1
    }
  },
  mounted() {
    this.loadDocsList()
  },
  methods: {
    handleFileChange(event) {
      const files = event.target.files
      if (!files || !files.length) return

      this.selectedFile = files[0]
      this.fileId = ''
      this.parsedText = ''
      this.summaryText = ''
      this.message = ''
      this.parseResult = null
    },

    openUploadConfigDialog() {
      if (!this.selectedFile) {
        this.message = '请先选择文件'
        return
      }

      this.configDialogMode = 'upload'
      this.currentConfigDoc = null
      this.showConfigDialog = true
      this.message = '请设置解析参数，点击确定后将自动上传并开始解析'
    },

    async doUploadAndParse(config) {
      if (!this.selectedFile) {
        this.message = '请先选择文件'
        return
      }

      try {
        this.uploading = true
        this.parsing = true
        this.message = '正在上传文件并开始解析，请稍候...'

        const uploadRes = await uploadFile(this.selectedFile)
        this.fileId = uploadRes.data?.file_id || ''

        if (!this.fileId) {
          throw new Error('上传成功但未返回 file_id')
        }

        const parseRes = await parseFile(this.fileId, config)
        this.parseResult = parseRes.data || {}
        this.parsedText = parseRes.data?.text || parseRes.data?.content || ''
        this.summaryText = ''
        this.message = parseRes.message || '解析完成'

        await this.loadDocsList()
      } catch (error) {
        this.message = `上传解析失败：${error.message}`
      } finally {
        this.uploading = false
        this.parsing = false
      }
    },

    async handleGenerateSelectedSummary() {
      if (!this.selectedDocIds.length) {
        this.message = '请先选择一个文档'
        return
      }

      if (this.selectedDocIds.length > 1) {
        this.message = '当前版本一次只支持选择 1 个文档生成摘要'
        return
      }

      const docId = this.selectedDocIds[0]

      try {
        this.summarizing = true
        this.message = '正在获取文档内容并生成摘要，请稍候...'

        let detailData = null

        if (
          this.currentDoc &&
          this.currentDoc.docId === docId &&
          this.currentDoc.detailData &&
          Array.isArray(this.currentDoc.detailData.contentList)
        ) {
          detailData = this.currentDoc.detailData
        } else {
          const detailRes = await getDocDetail({
            docId,
            keyword: '',
            pageNo: 1,
            pageSize: 50
          })
          detailData = detailRes.data || {}
        }

        const contentList = detailData.contentList || []

        if (!contentList.length) {
          this.message = '当前文档没有可用于摘要的分段内容'
          return
        }

        const fullText = contentList
          .map(item => item.content || '')
          .filter(Boolean)
          .join('\n\n')
          .slice(0, 12000)

        if (!fullText.trim()) {
          this.message = '当前文档分段内容为空，无法生成摘要'
          return
        }

        const summaryRes = await generateSummary(fullText)
        this.summaryText = summaryRes.data?.summary || ''
        this.message = summaryRes.message || '摘要生成成功'
      } catch (error) {
        this.message = `生成摘要失败：${error.message}`
      } finally {
        this.summarizing = false
      }
    },

    async loadDocsList() {
      try {
        this.loadingDocs = true
        const res = await getDocsList()
        this.docsList = res.data?.list || []

        const validIds = this.docsList.map(item => item.docId)
        this.selectedDocIds = this.selectedDocIds.filter(id => validIds.includes(id))
      } catch (error) {
        this.message = `获取文档列表失败：${error.message}`
      } finally {
        this.loadingDocs = false
      }
    },

    toggleSelectAll(event) {
      const checked = event.target.checked
      if (checked) {
        this.selectedDocIds = this.docsList.map(item => item.docId).filter(Boolean)
      } else {
        this.selectedDocIds = []
      }
    },

    toggleSelectDoc(docId) {
      if (!docId) return

      if (this.selectedDocIds.includes(docId)) {
        this.selectedDocIds = this.selectedDocIds.filter(id => id !== docId)
      } else {
        this.selectedDocIds = [...this.selectedDocIds, docId]
      }
    },

    async handleBatchDelete() {
      if (!this.selectedDocIds.length) {
        this.message = '请先选择要删除的文档'
        return
      }

      const ok = window.confirm(`确认删除已选中的 ${this.selectedDocIds.length} 个文档吗？`)
      if (!ok) return

      try {
        this.deletingBatch = true
        this.message = '正在批量删除文档...'

        await deleteDocs(this.selectedDocIds)
        this.message = '批量删除成功'
        this.currentDoc = null
        this.selectedDocIds = []

        await this.loadDocsList()
      } catch (error) {
        this.message = `批量删除失败：${error.message}`
      } finally {
        this.deletingBatch = false
      }
    },

    async handleDelete(item) {
      if (!item.docId) {
        this.message = '当前文档缺少 docId，无法删除'
        return
      }

      const ok = window.confirm(`确认删除文档《${item.fileName}》吗？`)
      if (!ok) return

      try {
        this.message = '正在删除文档...'
        await deleteDocs([item.docId])
        this.message = '删除文档成功'

        if (this.currentDoc && this.currentDoc.docId === item.docId) {
          this.currentDoc = null
        }

        this.selectedDocIds = this.selectedDocIds.filter(id => id !== item.docId)
        await this.loadDocsList()
      } catch (error) {
        this.message = `删除文档失败：${error.message}`
      }
    },

    async handleSegment(item) {
      if (!item.docId) {
        this.message = '当前文档缺少 docId，无法配置'
        return
      }

      try {
        this.message = '正在获取文档配置...'
        const res = await getDocConfig(item.docId)
        const data = res.data || {}

        this.configDialogMode = 'edit'
        this.currentConfigDoc = item
        this.fillConfigForm(data)
        this.showConfigDialog = true
        this.message = '获取文档配置成功'
      } catch (error) {
        this.message = `获取文档配置失败：${error.message}`
      }
    },

    async submitConfigDialog(payload) {
      try {
        this.savingConfig = true

        const config = this.buildSubmitConfig(payload)

        if (this.configDialogMode === 'upload') {
          this.configForm = JSON.parse(JSON.stringify(config))
          this.splitterText = payload.splitterText || this.splitterText
          this.subSplitterText = payload.subSplitterText || this.subSplitterText
          this.showConfigDialog = false

          await this.doUploadAndParse(config)
          return
        }

        if (!this.currentConfigDoc?.docId) {
          this.message = '当前文档信息缺失'
          return
        }

        this.message = '正在更新文档配置并重新解析...'

        await updateDocConfig([this.currentConfigDoc.docId], config)
        this.message = '更新文档配置成功，已提交重新解析'

        this.showConfigDialog = false
        this.currentConfigDoc = null

        await this.loadDocsList()
      } catch (error) {
        this.message = `更新文档配置失败：${error.message}`
      } finally {
        this.savingConfig = false
      }
    },

    closeConfigDialog() {
      this.showConfigDialog = false
      this.currentConfigDoc = null
    },

    fillConfigForm(data) {
      const docSegment = data.docSegment || {}

      this.configForm = {
        docImportType: data.docImportType ?? 0,
        docSegment: {
          segmentMethod: String(docSegment.segmentMethod ?? '0'),
          segmentType: String(docSegment.segmentType ?? '0'),
          splitter: docSegment.splitter || ['\\n\\n'],
          maxSplitter: docSegment.maxSplitter ?? 1024,
          overlap: docSegment.overlap ?? 0.2,
          subSplitter: docSegment.subSplitter || ['\\n'],
          subMaxSplitter: docSegment.subMaxSplitter ?? 4000
        },
        docAnalyzer: data.docAnalyzer || ['text'],
        parserModelId: data.parserModelId || '',
        docPreprocess: data.docPreprocess || ['replaceSymbols'],
        docMetaData: []
      }

      this.splitterText = (this.configForm.docSegment.splitter || []).join(',')
      this.subSplitterText = (this.configForm.docSegment.subSplitter || []).join(',')
    },

    buildSubmitConfig(payload) {
      const config = JSON.parse(JSON.stringify(payload.config))
      const splitterText = payload.splitterText || ''
      const subSplitterText = payload.subSplitterText || ''

      if (config.docSegment.segmentMethod === '0') {
        if (config.docSegment.segmentType === '1') {
          config.docSegment.splitter = this.parseSplitterText(splitterText)
        } else {
          delete config.docSegment.splitter
          delete config.docSegment.maxSplitter
          delete config.docSegment.overlap
        }

        delete config.docSegment.subSplitter
        delete config.docSegment.subMaxSplitter
      }

      if (config.docSegment.segmentMethod === '1') {
        config.docSegment.subSplitter = this.parseSplitterText(subSplitterText)
        delete config.docSegment.segmentType
        delete config.docSegment.splitter
        delete config.docSegment.maxSplitter
        delete config.docSegment.overlap
      }

      if (!config.parserModelId) {
        delete config.parserModelId
      }

      return config
    },

    parseSplitterText(text) {
      return (text || '')
        .split(',')
        .map(item => item.trim())
        .filter(Boolean)
    },

    async handleView(item) {
      if (!item.docId) {
        this.message = '当前文档缺少 docId，无法查看'
        return
      }

      try {
        this.message = '正在获取文档详情...'
        const res = await getDocDetail({
          docId: item.docId,
          keyword: '',
          pageNo: 1,
          pageSize: 20
        })

        this.currentDoc = {
          ...item,
          detailData: res.data || {}
        }

        this.message = '获取文档详情成功'
      } catch (error) {
        this.message = `获取文档详情失败：${error.message}`
      }
    }
  }
}
</script>

<style scoped src="../assets/styles/common.css"></style>
<style scoped src="../assets/styles/parse-demo.css"></style>