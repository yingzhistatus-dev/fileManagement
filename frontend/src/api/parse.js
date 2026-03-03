import request from '../utils/request'

export function parseFile(fileId, config = null) {
  return request({
    url: '/api/parse',
    method: 'post',
    data: {
      file_id: fileId,
      config
    }
  })
}