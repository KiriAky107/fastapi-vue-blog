import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
// import naive-ui (按需引入，后续按需配置)

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
