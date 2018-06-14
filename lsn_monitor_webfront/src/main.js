// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Element from 'element-ui'
Vue.prototype.HOST = '/api'
Vue.use(VueAxios, axios)
Vue.use(Element)

// or
import {
  Select,
  Button
  // ...
} from 'element-ui'

Vue.component(Select.name, Select)
Vue.component(Button.name, Button)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
