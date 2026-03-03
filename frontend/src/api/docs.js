import request from '../utils/request'

export function getDocsList() {
  return request({
    url: '/api/docs/list',
    method: 'get'
  })
}

export function deleteDocs(docIdList) {
  return request({
    url: '/api/docs',
    method: 'delete',
    data: {
      docIdList
    }
  })
}

export function getDocDetail(params) {
  return request({
    url: '/api/docs/detail',
    method: 'get',
    params
  })
}

export function getDocConfig(docId) {
  return request({
    url: '/api/docs/config',
    method: 'get',
    params: {
      docId
    }
  })
}

export function updateDocConfig(docIdList, config) {
  return request({
    url: '/api/docs/update-config',
    method: 'post',
    data: {
      docIdList,
      config
    }
  })
}