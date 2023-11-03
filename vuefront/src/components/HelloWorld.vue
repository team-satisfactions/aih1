<template>
  <div class="hello">
    <XyzTransitionGroup class="item-group" xyz="stagger-2 narrow-100%">
      <h1 class="square" v-if="spell">{{ spell }}</h1>
      <h1 class="square" v-if="spell">↓</h1>
      <h1 class="square" v-if="command">$ {{ command }}</h1>
      <h1 class="square" v-if="command">↓</h1>
      <h1 class="square" v-if="commandResult">{{ commandResult }}</h1>
    </XyzTransitionGroup>
  </div>
  <div class="overlay" :class="bcolor">
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import { nextTick, ref, onMounted, watch, watchEffect} from 'vue'
//import VueAnimXyz from '@animxyz/vue3'
export default {
  name: 'HelloWorld',
  data(){
    return {
      message : 'aaa'
    }
  },
  props: {
    msg: String
  },
  setup(){
    const anime = ref(false)
    setInterval(() => {
      anime.value = !anime.value
    }, 1000);
    const bcolor = ref('')
    const spell = ref('')
    const command = ref('')
    const commandResult = ref('')
    onMounted(() => {
      console.log(`initial`)
      let int_id = NaN;
      let interval = ()=> {
        return setTimeout(()=>{
          axios.get('http://localhost:8000/reserved-spell')
          .then(async res => {
            clearTimeout(int_id)
            let data = res.data
            console.log(data)
            bcolor.value = ''
            spell.value = ''
            command.value = ''
            commandResult.value = ''
            await nextTick()
            sussess(data)
          }).catch(err => {
            console.log(err)
            int_id = interval()
          })
        }, 200)
      }
      int_id = interval()
      let sussess = (data)=>{
        spell.value = data.spell
        const succeeded = data.succeeded
        console.log({succeeded})
        setTimeout(()=>{
          command.value = data.command
          if(succeeded) {
            console.log(int_id)
            console.log(spell.value,command.value)
            console.log(`command changed`)
            setTimeout(()=>{
              axios.post('http://localhost:8000/chant-spell').then(res => {
                commandResult.value = res.data
                console.log(res)
                console.log(spell.value,command.value)
                setTimeout(() => {
                  bcolor.value = 'green'
                }, 1100);

                setTimeout(() => {
                  int_id = interval()
                }, 2000);
              }).catch(err => {
                console.log(err)
              });
            },2000)
          } else {
            commandResult.value = 'x'
            setTimeout(() => {
              bcolor.value = 'red'
            }, 1100);
            setTimeout(() => {
              int_id = interval()
            }, 2000);
          }
        }, 2000);
      }
    })
    return { spell, command, commandResult, anime, bcolor }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.item-group {
  --xyz-translate-y: -350%;
  --xyz-ease: cubic-bezier(0.5, -1.5, 0.5, 1.5);
}
.overlay {
  position: absolute;
  top: 0;
  left:0;
  right:0;
  bottom:0;
}
.red {
  background-color: rgba(255,0,0,0.2);
}
.green {
  background-color: rgba(0,255,0,0.2);
}
</style>
