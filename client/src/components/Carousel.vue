<template>
  <div class='carousel-view'>
      <transition-group
        class='carousel'
        tag="div">
        <div
          v-for="slide in slides"
          class='slide'
          :key="slide.id">
          <h4> {{ slide.title }} </h4>
        </div>
      </transition-group>
      <div class='carousel-controls'>
        <button class='carousel-controls__button' @click="previous">prev</button>
        <button class='carousel-controls__button' @click="next">next</button>
      </div>
    </div>
</template>

<script>
export default {
  name: 'MyCarousel',
  mounted() {
    console.log('hello')
  },
  data () {
    let s = JSON.parse(localStorage['web3registered_auctions']).addresses;
    return {
      slides: [
        {
          title: s[0],
          id: 1
        },
        {
          title: s[1],
          id: 2
        },
        {
          title: s[2],
          id: 3
        },
        {
          title: s[3],
          id: 4
        },
        {
          title: s[4],
          id: 5
        }
      ]
    }
  },
  methods: {
    next () {
      const first = this.slides.shift()
      this.slides = this.slides.concat(first)
    },
    previous () {
      const last = this.slides.pop()
      this.slides = [last].concat(this.slides)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.carousel-view {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.carousel {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;

  width: 24em;
  min-height: 25em;
}
.slide {
  flex: 0 0 20em;
  height: 20em;
  margin: 1em;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 0.1em dashed #000;
  border-radius: 50%;
  transition: transform 0.3s ease-in-out;
}
.slide:first-of-type {
  opacity: 0;
}
.slide:last-of-type {
  opacity: 0;
}
</style>
