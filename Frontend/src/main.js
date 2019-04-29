import Vue from 'vue'
import App from './App.vue'
import Router from './router';
import VueImg from 'v-img';

Vue.config.productionTip = false;
Vue.use(VueImg);

import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue);


import { Navbar } from 'bootstrap-vue/es/components';

Vue.use(Navbar); 

import { Button } from 'bootstrap-vue/es/components';

import autoRotate from 'vue-jpeg-auto-rotation';

Vue.use(autoRotate);

Vue.use(Button);

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

new Vue({
  router: Router,
  render: h => h(App),
}).$mount('#app');

