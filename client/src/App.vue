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
    /*
    this.$axios
      .get('http://127.0.0.1:5000/auction/abi')
      .then(response => (this.info = response))
    console.log('hello from App')
    console.log(this.info)*/
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
