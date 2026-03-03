import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 30000
})

// 请求拦截
request.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message =
      error?.response?.data?.message ||
      error?.response?.data?.detail ||
      error.message ||
      '请求失败'
    return Promise.reject(new Error(message))
  }
)

export default request