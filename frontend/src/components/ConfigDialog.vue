<template>
  <div v-if="visible" class="dialog-mask">
    <div class="dialog-card">
      <div class="dialog-header">
        <h3>{{ title }}</h3>
        <button class="icon-close" @click="$emit('close')">×</button>
      </div>

      <div class="dialog-body">
        <div class="config-section">
          <h4>分段方法</h4>
          <div class="option-grid two-cols">
            <label class="option-card" :class="{ active: localConfig.docSegment.segmentMethod === '0' }">
              <input type="radio" value="0" v-model="localConfig.docSegment.segmentMethod" />
              <div class="option-title">通用分段</div>
              <div class="option-desc">检索和召回的分段内容相同</div>
            </label>

            <label class="option-card" :class="{ active: localConfig.docSegment.segmentMethod === '1' }">
              <input type="radio" value="1" v-model="localConfig.docSegment.segmentMethod" />
              <div class="option-title">父子分段</div>
              <div class="option-desc">父分段用作上下文，子分段用于检索</div>
            </label>
          </div>
        </div>

        <div class="config-section" v-if="localConfig.docSegment.segmentMethod === '0'">
          <h4>分段方式配置</h4>
          <div class="option-grid two-cols">
            <label class="option-card" :class="{ active: localConfig.docSegment.segmentType === '0' }">
              <input type="radio" value="0" v-model="localConfig.docSegment.segmentType" />
              <div class="option-title">自动分段</div>
              <div class="option-desc">系统按默认方式分段</div>
            </label>

            <label class="option-card" :class="{ active: localConfig.docSegment.segmentType === '1' }">
              <input type="radio" value="1" v-model="localConfig.docSegment.segmentType" />
              <div class="option-title">自定义分段</div>
              <div class="option-desc">手动配置分段符和长度参数</div>
            </label>
          </div>
        </div>

        <div
          class="config-section"
          v-if="localConfig.docSegment.segmentMethod === '0' && localConfig.docSegment.segmentType === '1'"
        >
          <h4>自定义分段参数</h4>

          <div class="form-row">
            <label>分段标识</label>
            <input type="text" v-model="localSplitterText" placeholder="例如：\n\n,\n" />
            <small>多个分隔符用英文逗号分隔，例如：\n\n,\n</small>
          </div>

          <div class="form-row">
            <label>可分割最大值</label>
            <input type="number" v-model.number="localConfig.docSegment.maxSplitter" />
          </div>

          <div class="form-row">
            <label>可重叠值</label>
            <input type="number" step="0.1" v-model.number="localConfig.docSegment.overlap" />
          </div>
        </div>

        <div class="config-section" v-if="localConfig.docSegment.segmentMethod === '1'">
          <h4>父子分段参数</h4>

          <div class="form-row">
            <label>子分段标识</label>
            <input type="text" v-model="localSubSplitterText" placeholder="例如：\n" />
            <small>多个分隔符用英文逗号分隔</small>
          </div>

          <div class="form-row">
            <label>子可分割最大值</label>
            <input type="number" v-model.number="localConfig.docSegment.subMaxSplitter" />
          </div>
        </div>

        <div class="config-section">
          <h4>文本预处理规则</h4>
          <div class="checkbox-group">
            <label>
              <input type="checkbox" value="replaceSymbols" v-model="localConfig.docPreprocess" />
              替换连续的空格、换行符和制表符
            </label>
            <label>
              <input type="checkbox" value="deleteLinks" v-model="localConfig.docPreprocess" />
              删除所有 URL 和电子邮件地址
            </label>
          </div>
        </div>

        <div class="config-section">
          <h4>解析方式</h4>
          <div class="checkbox-group">
            <label>
              <input type="checkbox" value="text" v-model="localConfig.docAnalyzer" />
              文字提取
            </label>
            <label>
              <input type="checkbox" value="ocr" v-model="localConfig.docAnalyzer" />
              启用 OCR 解析
            </label>
            <label>
              <input type="checkbox" value="model" v-model="localConfig.docAnalyzer" />
              模型解析
            </label>
          </div>
        </div>

        <div class="form-row" v-if="localConfig.docAnalyzer.includes('ocr') || localConfig.docAnalyzer.includes('model')">
          <label>解析模型ID（可选）</label>
          <input type="text" v-model="localConfig.parserModelId" placeholder="可不填" />
        </div>
      </div>

      <div class="dialog-footer">
        <button class="btn btn-default" @click="$emit('close')">取消</button>
        <button class="btn btn-success" :disabled="saving" @click="handleSubmit">
          {{ saving ? '提交中...' : '确定' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfigDialog',
  props: {
    visible: Boolean,
    saving: Boolean,
    title: {
      type: String,
      default: '分段设置'
    },
    config: {
      type: Object,
      default: () => ({})
    },
    splitterText: {
      type: String,
      default: '\\n\\n'
    },
    subSplitterText: {
      type: String,
      default: '\\n'
    }
  },
  emits: ['close', 'submit'],
  data() {
    return {
      localConfig: this.cloneConfig(this.config),
      localSplitterText: this.splitterText,
      localSubSplitterText: this.subSplitterText
    }
  },
  watch: {
    config: {
      deep: true,
      immediate: true,
      handler(val) {
        this.localConfig = this.cloneConfig(val)
      }
    },
    splitterText(val) {
      this.localSplitterText = val
    },
    subSplitterText(val) {
      this.localSubSplitterText = val
    }
  },
  methods: {
    cloneConfig(config) {
      return JSON.parse(JSON.stringify(config || {
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
      }))
    },
    handleSubmit() {
      this.$emit('submit', {
        config: this.localConfig,
        splitterText: this.localSplitterText,
        subSplitterText: this.localSubSplitterText
      })
    }
  }
}
</script>

<style scoped src="../assets/styles/common.css"></style>
<style scoped src="../assets/styles/config-dialog.css"></style>