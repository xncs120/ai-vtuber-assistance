# Vue 3 + Vite + TailwindCss + DaisyUi

# How to setup
pnpm create vite@latest ui
cd ui
pnpm install OR pnpm install tailwindcss @tailwindcss/vite daisyui vue-router vuex
// vite.config.js
import tailwindcss from '@tailwindcss/vite'
plugins: [
  vue(),
  tailwindcss(),
]
// src/style.css (custom design https://daisyui.com/theme-generator/?lang=en)
@import "tailwindcss";
@plugin "daisyui";
@plugin "daisyui/theme" {
  name: "vuedark";
  default: true;
  prefersdark: true;
  color-scheme: "dark";
  --color-base-100: oklch(23.93% 0.000 0);
  --color-base-200: oklch(20.90% 0.000 0);
  --color-base-300: oklch(37% 0 0);
  --color-base-content: oklch(97.807% 0.029 256.847);
  --color-primary: oklch(70.48% 0.158 160.55);
  --color-primary-content: oklch(96% 0.018 272.314);
  --color-secondary: oklch(65% 0.241 354.308);
  --color-secondary-content: oklch(94% 0.028 342.258);
  --color-accent: oklch(77% 0.152 181.912);
  --color-accent-content: oklch(38% 0.063 188.416);
  --color-neutral: oklch(14% 0.005 285.823);
  --color-neutral-content: oklch(92% 0.004 286.32);
  --color-info: oklch(74% 0.16 232.661);
  --color-info-content: oklch(29% 0.066 243.157);
  --color-success: oklch(76% 0.177 163.223);
  --color-success-content: oklch(37% 0.077 168.94);
  --color-warning: oklch(82% 0.189 84.429);
  --color-warning-content: oklch(41% 0.112 45.904);
  --color-error: oklch(71% 0.194 13.428);
  --color-error-content: oklch(27% 0.105 12.094);
  --radius-selector: 0.5rem;
  --radius-field: 0.25rem;
  --radius-box: 0.5rem;
  --size-selector: 0.25rem;
  --size-field: 0.25rem;
  --border: 1px;
  --depth: 1;
  --noise: 0;
}
.input:focus,
.select:focus,
.textarea:focus,
.button:focus {
  outline: none !important;
  box-shadow: none !important;
  border-color: inherit !important;
}
// index.html
<html lang="en" data-theme="vuedark">
// create /src/store/index.js and write in below example
import { createStore } from 'vuex'
const store = createStore({
  state() {
    return {}
  },
  mutations: {,
  actions: {},
  getters: {},
})
export default store
// main.js (integrate vue-router vuex)
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

# PIXI + Live2D Cubism4
// https://www.npmjs.com/package/pixi-live2d-display-lipsyncpatch
pnpm install pixi.js@^7 pixi-live2d-display-lipsyncpatch
download live2dcubismcore.min.js and place in /public/lib/live2dcubismcore.min.js
download live 2d model with cubism4 support and place in /public/models/...
// Live2DViewer.vue
import * as PIXI from 'pixi.js'
import { Live2DModel } from 'pixi-live2d-display-lipsyncpatch/cubism4';
window.PIXI = PIXI
onMounted(async () => {
  const app = new PIXI.Application({
    view: live2dCanvas.value,
    autoStart: true,
    resizeTo: window
  })
  const model = await Live2DModel.from('/models/poblanc/Poblanc.model3.json')
  app.stage.addChild(model)
  model.x = window.innerWidth / 2
  model.y = window.innerHeight / 2
})

# other package
dayjs marked