<template>
  <div class="graph-page">
    <div class="card">
      <div class="page-header">
        <div>
          <h2>知识图谱</h2>
          <p class="desc">展示当前知识库的实体关系网络与统计信息。</p>
        </div>
        <button class="btn" :disabled="loading" @click="loadGraph">
          {{ loading ? '加载中...' : '刷新图谱' }}
        </button>
      </div>

      <div class="message" v-if="message">
        {{ message }}
      </div>

      <div class="stats-grid" v-if="graphData">
        <div class="stat-card">
          <div class="stat-label">知识库ID</div>
          <div class="stat-value break">{{ graphData.knowledgeId || '-' }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">处理中文档</div>
          <div class="stat-value">{{ graphData.processingCount ?? 0 }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">成功文档</div>
          <div class="stat-value">{{ graphData.successCount ?? 0 }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">失败文档</div>
          <div class="stat-value">{{ graphData.failCount ?? 0 }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">总文档数</div>
          <div class="stat-value">{{ graphData.total ?? 0 }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">实体数</div>
          <div class="stat-value">{{ nodes.length }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">关系数</div>
          <div class="stat-value">{{ edges.length }}</div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="section-header">
        <h3>图谱可视化</h3>
      </div>

      <div ref="chartRef" class="graph-chart"></div>
    </div>

    <div class="card">
      <div class="section-header">
        <h3>实体列表</h3>
        <input
          v-model="nodeKeyword"
          class="search-input"
          placeholder="搜索实体名称"
        />
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>实体名称</th>
              <th>实体类型</th>
              <th>来源文件</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="node in filteredNodes" :key="node.entity_name">
              <td>{{ node.entity_name }}</td>
              <td>{{ node.entity_type || '-' }}</td>
              <td>{{ formatSource(node.source_id) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div class="section-header">
        <h3>关系列表</h3>
        <input
          v-model="edgeKeyword"
          class="search-input"
          placeholder="搜索关系描述/实体"
        />
      </div>

      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>源实体</th>
              <th>目标实体</th>
              <th>关系</th>
              <th>权重</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="edge in filteredEdges" :key="`${edge.source_entity}-${edge.target_entity}-${edge.description}`">
              <td>{{ edge.source_entity }}</td>
              <td>{{ edge.target_entity }}</td>
              <td>{{ edge.description || '-' }}</td>
              <td>{{ edge.weight ?? 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getKnowledgeGraph } from '../api/graph'

export default {
  name: 'GraphDemo',
  data() {
    return {
      loading: false,
      message: '',
      graphData: null,
      nodeKeyword: '',
      edgeKeyword: '',
      chart: null
    }
  },
  computed: {
    nodes() {
      return this.graphData?.graph?.nodes || []
    },
    edges() {
      return this.graphData?.graph?.edges || []
    },
    filteredNodes() {
      const keyword = this.nodeKeyword.trim().toLowerCase()
      if (!keyword) return this.nodes
      return this.nodes.filter(item =>
        (item.entity_name || '').toLowerCase().includes(keyword)
      )
    },
    filteredEdges() {
      const keyword = this.edgeKeyword.trim().toLowerCase()
      if (!keyword) return this.edges
      return this.edges.filter(item =>
        (item.source_entity || '').toLowerCase().includes(keyword) ||
        (item.target_entity || '').toLowerCase().includes(keyword) ||
        (item.description || '').toLowerCase().includes(keyword)
      )
    }
  },
  mounted() {
    this.initChart()
    this.loadGraph()
    window.addEventListener('resize', this.handleResize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
  },
  methods: {
    async loadGraph() {
      try {
        this.loading = true
        this.message = '正在加载知识图谱...'

        const res = await getKnowledgeGraph()
        this.graphData = res.data || null
        this.message = res.message || '获取知识图谱成功'

        this.renderChart()
      } catch (error) {
        this.message = `获取知识图谱失败：${error.message}`
      } finally {
        this.loading = false
      }
    },

    initChart() {
      if (this.$refs.chartRef) {
        this.chart = echarts.init(this.$refs.chartRef)
      }
    },

    handleResize() {
      this.chart && this.chart.resize()
    },

    renderChart() {
      if (!this.chart) {
        this.initChart()
      }
      if (!this.chart) return

      const nodes = (this.nodes || []).map((item, index) => ({
        id: item.entity_name,
        name: item.entity_name,
        value: (item.source_id || []).length || 1,
        category: item.entity_type || 'entity',
        symbolSize: Math.max(26, Math.min(60, 20 + ((item.source_id || []).length * 6))),
        label: {
          show: true
        }
      }))

      const links = (this.edges || []).map(item => ({
        source: item.source_entity,
        target: item.target_entity,
        value: item.description || '',
        lineStyle: {
          width: Math.max(1, item.weight || 1)
        },
        label: {
          show: true,
          formatter: item.description || ''
        }
      }))

      const option = {
        tooltip: {
          formatter: params => {
            if (params.dataType === 'edge') {
              return `${params.data.source} → ${params.data.target}<br/>关系：${params.data.value || '-'}`
            }
            return `实体：${params.data.name}<br/>关联文件数：${params.data.value || 0}`
          }
        },
        animationDuration: 1000,
        series: [
          {
            type: 'graph',
            layout: 'force',
            roam: true,
            draggable: true,
            data: nodes,
            links,
            force: {
              repulsion: 320,
              edgeLength: [120, 220]
            },
            emphasis: {
              focus: 'adjacency'
            },
            lineStyle: {
              opacity: 0.8,
              curveness: 0.08
            },
            label: {
              position: 'right'
            }
          }
        ]
      }

      this.chart.setOption(option)
    },

    formatSource(sourceList) {
      if (!Array.isArray(sourceList) || !sourceList.length) return '-'
      return sourceList.join('；')
    }
  }
}
</script>

<style scoped>
.graph-page {
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
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.desc {
  color: #666;
  margin-top: 8px;
  margin-bottom: 0;
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

.message {
  padding: 12px 14px;
  background: #eef4ff;
  color: #1f3b75;
  border-radius: 8px;
  margin-bottom: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.stat-card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px 16px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.break {
  word-break: break-all;
  font-size: 14px;
}

.graph-chart {
  width: 100%;
  height: 700px;
}

.search-input {
  width: 260px;
  border: 1px solid #dbe3ee;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  text-align: left;
  padding: 14px 12px;
  border-bottom: 1px solid #edf0f2;
  font-size: 14px;
  vertical-align: top;
}

.data-table th {
  background: #fafafa;
  color: #475569;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .graph-chart {
    height: 560px;
  }
}

@media (max-width: 768px) {
  .page-header,
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .search-input {
    width: 100%;
  }

  .graph-chart {
    height: 480px;
  }
}
</style>