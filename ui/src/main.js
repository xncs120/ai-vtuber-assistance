import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import store from './store'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: App },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')