import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ParseDemo from '../views/ParseDemo.vue'
import GraphDemo from '../views/GraphDemo.vue'
import ReportDemo from '../views/ReportDemo.vue'
import ChatDemo from '../views/ChatDemo.vue'
import ChatEmbed from '../views/ChatEmbed.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/parse',
    name: 'ParseDemo',
    component: ParseDemo
  },
  {
    path: '/graph',
    name: 'GraphDemo',
    component: GraphDemo
  },
  {
    path: '/report',
    name: 'ReportDemo',
    component: ReportDemo
  },
  {
    path: '/chat',
    name: 'ChatDemo',
    component: ChatDemo
  },
  {
    path: '/chat-embed',
    name: 'ChatEmbed',
    component: ChatEmbed
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router