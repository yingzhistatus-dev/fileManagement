<template>
  <div class="table-card">
    <div class="table-header">
      <h3>当前知识库文档列表</h3>
    </div>

    <div class="empty-box" v-if="!docsList.length && !loadingDocs">
      当前知识库暂无文档
    </div>

    <div class="table-wrapper" v-else>
      <table class="result-table">
        <thead>
          <tr>
            <th class="checkbox-col">
              <input
                type="checkbox"
                :checked="isAllSelected"
                :indeterminate.prop="isIndeterminate"
                @change="$emit('toggle-select-all', $event)"
              />
            </th>
            <th>文件名称</th>
            <th>文件类型</th>
            <th>解析模式</th>
            <th>分段模式</th>
            <th>上传时间</th>
            <th>当前状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in docsList" :key="item.docId || item.fileName">
            <td class="checkbox-col">
              <input
                type="checkbox"
                :checked="selectedDocIds.includes(item.docId)"
                @change="$emit('toggle-select-doc', item.docId)"
              />
            </td>
            <td class="file-name-cell" :title="item.fileName">{{ item.fileName }}</td>
            <td>{{ item.fileType }}</td>
            <td>{{ item.parseMode || '-' }}</td>
            <td>{{ formatSegmentMode(item.segmentMode) }}</td>
            <td>{{ item.uploadTime || '-' }}</td>
            <td>
              <span
                class="status-tag"
                :class="{
                  success: item.statusText === '处理完成' || item.statusText === '解析成功',
                  pending: item.statusText === '正在解析中' || item.statusText === '处理中',
                  fail: item.statusText === '解析失败'
                }"
              >
                {{ item.statusText }}
              </span>
            </td>
            <td>
              <div class="op-group">
                <button class="table-btn" @click="$emit('delete-doc', item)">删除</button>
                <button class="table-btn" @click="$emit('segment-doc', item)">分段设置</button>
                <button class="table-btn" @click="$emit('view-doc', item)">查看</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DocTable',
  props: {
    docsList: {
      type: Array,
      default: () => []
    },
    selectedDocIds: {
      type: Array,
      default: () => []
    },
    loadingDocs: Boolean,
    isAllSelected: Boolean,
    isIndeterminate: Boolean
  },
  emits: [
    'toggle-select-all',
    'toggle-select-doc',
    'delete-doc',
    'segment-doc',
    'view-doc'
  ],
  methods: {
    formatSegmentMode(value) {
      if (value === 0 || value === '0') return '通用分段'
      if (value === 1 || value === '1') return '父子分段'
      return value || '通用分段'
    }
  }
}
</script>

<style scoped src="../assets/styles/common.css"></style>
<style scoped src="../assets/styles/doc-table.css"></style>