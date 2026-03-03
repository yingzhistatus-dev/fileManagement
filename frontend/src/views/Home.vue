<template>
  <div class="home-page">
    <div class="card">
      <h2>欢迎使用 Filemanagement Demo</h2>
      <p>这是一个基于知识库能力构建的文件管理与知识增强演示系统。</p>
    </div>

    <div class="card-grid">
      <router-link to="/parse" class="entry-card">
        <h3>文件解析</h3>
        <p>上传文件、配置解析参数、导入知识库、查看文档详情与生成摘要。</p>
      </router-link>

      <router-link to="/graph" class="entry-card">
        <h3>知识图谱</h3>
        <p>查看知识库中的实体、关系以及图谱可视化结果。</p>
      </router-link>

      <router-link to="/report" class="entry-card">
        <h3>社区报告</h3>
        <p>查看社区报告生成状态、报告卡片和详细内容。</p>
      </router-link>

      <router-link to="/chat" class="entry-card">
        <h3>文本问答</h3>
        <p>使用你自己接入的智能体 API 进行持久化问答。</p>
      </router-link>

      <router-link to="/chat-embed" class="entry-card">
        <h3>问答嵌入</h3>
        <p>直接嵌入万悟 WebChat 页面，快速复用现成问答界面。</p>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  margin-bottom: 20px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.entry-card {
  display: block;
  text-decoration: none;
  color: inherit;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.entry-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
}

.entry-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #111827;
}

.entry-card p {
  margin: 0;
  color: #6b7280;
  line-height: 1.7;
}

@media (max-width: 900px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>