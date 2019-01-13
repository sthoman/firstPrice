<template>
  <div id="app">
    <MyCarousel msg="test"/>
  </div>
</template>

<script>
import MyCarousel from './components/Carousel.vue'
export default {
  name: 'app',
  components: {
    MyCarousel
  },
  mounted(){
    console.log('hello from App')
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
