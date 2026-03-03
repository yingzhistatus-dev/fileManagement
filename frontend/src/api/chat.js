import request from '../utils/request'

export function createConversation(title) {
  return request({
    url: '/api/chat/conversation',
    method: 'post',
    data: { title }
  })
}

export function sendChatMessage(conversationId, query, stream = false) {
  return request({
    url: '/api/chat/message',
    method: 'post',
    timeout: 120000,
    data: {
      conversation_id: conversationId,
      query,
      stream
    }
  })
}