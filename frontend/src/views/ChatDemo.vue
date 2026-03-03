<template>
  <div class="chat-page">
    <div class="card">
      <div class="page-header">
        <div>
          <h2>文本问答</h2>
          <p class="desc">基于万悟智能体 API 的持久化对话问答。</p>
        </div>
        <button class="btn btn-default" @click="resetConversation">新建会话</button>
      </div>

      <div class="message" v-if="message">{{ message }}</div>

      <div class="conversation-box">
        <div class="meta-row">
          <span class="meta-label">会话标题：</span>
          <input
            v-model="conversationTitle"
            class="title-input"
            placeholder="请输入会话标题"
          />
        </div>

        <div class="meta-row">
          <span class="meta-label">会话ID：</span>
          <span class="meta-value">{{ conversationId || '未创建' }}</span>
        </div>
      </div>

      <div class="chat-history">
        <div
          v-for="(item, index) in chatMessages"
          :key="index"
          class="chat-item"
        >
          <div class="chat-query">
            <div class="chat-role user">用户</div>
            <div class="chat-bubble user-bubble">{{ item.query }}</div>
          </div>

          <div class="chat-response">
            <div class="chat-role bot">智能体</div>
            <div class="chat-bubble bot-bubble">{{ item.response }}</div>
          </div>
        </div>

        <div class="empty-box" v-if="!chatMessages.length">
          当前还没有对话，先输入一个问题试试。
        </div>
      </div>

      <div class="input-area">
        <textarea
          v-model="queryText"
          rows="4"
          placeholder="请输入你的问题"
        ></textarea>

        <div class="input-actions">
          <button class="btn" :disabled="sending" @click="handleSend">
            {{ sending ? '发送中...' : '发送问题' }}
          </button>
        </div>
      </div>
    </div>

    <div class="card" v-if="lastResult">
      <h3>知识增强结果</h3>

      <div class="usage-box" v-if="lastResult.usage">
        <span>prompt_tokens: {{ lastResult.usage.prompt_tokens ?? 0 }}</span>
        <span>completion_tokens: {{ lastResult.usage.completion_tokens ?? 0 }}</span>
        <span>total_tokens: {{ lastResult.usage.total_tokens ?? 0 }}</span>
      </div>

      <div v-if="Array.isArray(lastResult.search_list) && lastResult.search_list.length">
        <div
          v-for="(item, index) in lastResult.search_list"
          :key="index"
          class="search-card"
        >
          <div class="search-title">{{ item.title || '未命名片段' }}</div>
          <div class="search-kb">知识库：{{ item.kb_name || '-' }}</div>
          <div class="search-snippet">{{ item.snippet || '-' }}</div>
        </div>
      </div>

      <div class="empty-box" v-else>
        当前问题没有返回知识片段。
      </div>
    </div>
  </div>
</template>

<script>
import { createConversation, sendChatMessage } from '../api/chat'

export default {
  name: 'ChatDemo',
  data() {
    return {
      conversationTitle: '新建文本问答',
      conversationId: '',
      queryText: '',
      sending: false,
      message: '',
      chatMessages: [],
      lastResult: null
    }
  },
  methods: {
    async ensureConversation() {
      if (this.conversationId) return this.conversationId

      const res = await createConversation(this.conversationTitle || '新建文本问答')
      const conversationId = res?.data?.conversation_id || ''
      if (!conversationId) {
        throw new Error('创建对话成功，但未返回 conversation_id')
      }
      this.conversationId = conversationId
      return conversationId
    },

    async handleSend() {
      const query = this.queryText.trim()
      if (!query) {
        this.message = '请输入问题'
        return
      }

      try {
        this.sending = true
        this.message = '正在发送问题...'

        const conversationId = await this.ensureConversation()
        const res = await sendChatMessage(conversationId, query, false)
        const data = res?.data || {}

        const responseText = data.response || ''
        this.chatMessages.push({
          query,
          response: responseText || '未返回回答内容'
        })

        this.lastResult = data
        this.queryText = ''
        this.message = res?.message || '对话成功'
      } catch (error) {
        this.message = `对话失败：${error.message}`
      } finally {
        this.sending = false
      }
    },

    resetConversation() {
      this.conversationId = ''
      this.chatMessages = []
      this.lastResult = null
      this.queryText = ''
      this.message = '已重置当前会话'
    }
  }
}
</script>

<style scoped>
.chat-page {
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

.page-header {
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

.message {
  padding: 12px 14px;
  background: #eef4ff;
  color: #1f3b75;
  border-radius: 8px;
  margin-bottom: 16px;
}

.conversation-box {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.meta-row:last-child {
  margin-bottom: 0;
}

.meta-label {
  min-width: 80px;
  color: #64748b;
}

.meta-value {
  color: #111827;
  word-break: break-all;
}

.title-input {
  flex: 1;
  border: 1px solid #dbe3ee;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
}

.chat-history {
  margin-bottom: 20px;
}

.chat-item {
  margin-bottom: 18px;
  border-bottom: 1px solid #eef2f7;
  padding-bottom: 18px;
}

.chat-role {
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 8px;
}

.chat-role.user {
  color: #2563eb;
}

.chat-role.bot {
  color: #16a34a;
}

.chat-bubble {
  border-radius: 12px;
  padding: 14px 16px;
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
}

.user-bubble {
  background: #eff6ff;
  color: #1e3a8a;
}

.bot-bubble {
  background: #f0fdf4;
  color: #166534;
}

.input-area textarea {
  width: 100%;
  resize: vertical;
  border: 1px solid #dbe3ee;
  border-radius: 12px;
  padding: 12px;
  font-size: 14px;
  line-height: 1.8;
  box-sizing: border-box;
}

.input-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
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

.btn-default {
  background: #64748b;
}

.usage-box {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
  margin-bottom: 16px;
  color: #475569;
}

.search-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 12px;
  background: #fafafa;
}

.search-title {
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.search-kb {
  color: #475569;
  margin-bottom: 8px;
}

.search-snippet {
  color: #374151;
  line-height: 1.8;
  white-space: pre-wrap;
}

.empty-box {
  color: #64748b;
}

@media (max-width: 768px) {
  .page-header,
  .meta-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .title-input {
    width: 100%;
  }
}
</style>