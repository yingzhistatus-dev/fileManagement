import request from '../utils/request'

export function generateSummary(content) {
  return request({
    url: '/api/summary',
    method: 'post',
    timeout: 120000,
    data: {
      content
    }
  })
}