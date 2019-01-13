import Vue from 'vue'
import VueCarousel from 'vue-carousel';
import App from './App.vue'

Vue.config.productionTip = false
Vue.use(VueCarousel);

new Vue({
  render: h => h(App),
}).$mount('#app')
