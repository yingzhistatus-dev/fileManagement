<template>
  <div id="app">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-title">Filemanagement Demo</div>
        <div class="brand-subtitle">Wanwu Knowledge Base Demo</div>
      </div>

      <nav class="nav">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/parse" class="nav-item">文件解析</router-link>
        <router-link to="/graph" class="nav-item">知识图谱</router-link>
        <router-link to="/report" class="nav-item">社区报告</router-link>
        <router-link to="/chat" class="nav-item">文本问答</router-link>
        <router-link to="/chat-embed" class="nav-item">问答嵌入</router-link>
      </nav>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  background: #f5f7fb;
  color: #1f2937;
}

.sidebar {
  width: 240px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 24px 18px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.brand-title {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
}

.brand-subtitle {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.6;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: block;
  padding: 12px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #374151;
  font-weight: 600;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: #f3f4f6;
}

.nav-item.router-link-active {
  background: #eaf2ff;
  color: #1f6feb;
}

.main-content {
  flex: 1;
  padding: 24px;
  box-sizing: border-box;
  overflow-x: auto;
}

@media (max-width: 900px) {
  #app {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e5e7eb;
  }

  .nav {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .nav-item {
    width: auto;
  }
}
</style>