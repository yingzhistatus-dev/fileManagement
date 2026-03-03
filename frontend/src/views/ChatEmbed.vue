<template>
  <div class="chat-embed-page">
    <div class="toolbar">
      <div>
        <h2>问答嵌入</h2>
        <p class="desc">当前页面直接嵌入万悟 WebChat 页面。</p>
      </div>

      <a
        class="open-link"
        href="http://119.188.221.193:8081/aibase/webChat/b9dc0359-4df7-45a9-bc26-7d26449a3bc7"
        target="_blank"
        rel="noopener noreferrer"
      >
        新窗口打开
      </a>
    </div>

    <iframe
      class="chat-frame"
      src="http://119.188.221.193:8081/aibase/webChat/b9dc0359-4df7-45a9-bc26-7d26449a3bc7"
      frameborder="0"
    ></iframe>
  </div>
</template>

<script>
export default {
  name: 'ChatEmbed'
}
</script>

<style scoped>
.chat-embed-page {
  height: calc(100vh - 48px);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.desc {
  color: #666;
  margin-top: 8px;
}

.open-link {
  text-decoration: none;
  color: #1f6feb;
  font-weight: 600;
}

.chat-frame {
  flex: 1;
  width: 100%;
  min-height: 780px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
}
</style>