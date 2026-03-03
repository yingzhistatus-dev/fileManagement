import request from '../utils/request'

export function getReportList(params = {}) {
  return request({
    url: '/api/reports',
    method: 'get',
    params
  })
}

export function generateReport() {
  return request({
    url: '/api/reports/generate',
    method: 'post'
  })
}