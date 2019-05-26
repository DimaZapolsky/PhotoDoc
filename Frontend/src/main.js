import Vue from 'vue'
import App from './App.vue'
import Router from './router';

Vue.config.productionTip = false;

import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue);


import { Navbar } from 'bootstrap-vue/es/components';

Vue.use(Navbar); 

import { Button } from 'bootstrap-vue/es/components';

Vue.use(Button);

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import Croppa from 'vue-croppa'

 Vue.use(Croppa)            

new Vue({
  router: Router,
  render: h => h(App),
}).$mount('#app');

