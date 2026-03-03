import request from '../utils/request'

export function getKnowledgeGraph() {
  return request({
    url: '/api/graph',
    method: 'get',
    timeout: 120000
  })
}