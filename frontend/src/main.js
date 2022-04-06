import { createApp } from 'vue'
import App from './App.vue'
import { createWebHistory, createRouter } from "vue-router";
import Toaster from '@meforma/vue-toaster';
import Home from './views/Home.vue'
import View from './views/View.vue'


const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/view/:coub_id",
    name: "Coub",
    component: View,
  },
  {
    path: "/:catchAll(.*)",
    redirect: '/',
  }
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