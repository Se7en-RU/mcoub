import { createApp } from 'vue'
import App from './App.vue'
import { createWebHistory, createRouter } from "vue-router";
import Toaster from '@meforma/vue-toaster';

const routes = [
  {
    path: "/",
    name: "Home",
    component: {},
  },
  {
    path: "/view/:coub_id",
    name: "Coub",
    component: {},
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App)
  .use(router)
  .use(Toaster, {
    position: 'top-right'
  })
  .mount('#app')