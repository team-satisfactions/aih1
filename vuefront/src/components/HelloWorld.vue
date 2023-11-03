<template>
  <div class="hello">
    <template v-if="commandResult">
      <h1>{{ spell }}</h1>
      <h1>↓</h1>
      <h1>$ {{ command }}</h1>
      <h1>↓</h1>
      <h1>$ {{ commandResult }}</h1>
    </template>
    <template v-else-if="command">
      <h1>{{ spell }}</h1>
      <h1>↓</h1>
      <h1>$ {{ command }}</h1>
    </template>
    <template v-else>
      <h1>{{ spell }}</h1>
      <h1>↓</h1>
      <h1>{{ command }}</h1>
    </template>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import { ref, onMounted, watch, watchEffect} from 'vue'
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
    const spell = ref('')
    const command = ref('')
    const commandResult = ref('')
    onMounted(() => {
      console.log(`initial`)
      let int_id = NaN;
      let interval = ()=> {
        return setTimeout(()=>{
          commandResult.value = '';
          //axios.get('http://192.168.106.214:8000/reserved-spell')
          axios.get('http://localhost:8000/reserved-spell')
          .then(res => {
            clearTimeout(int_id)
            let data = res.data
            console.log(data)
            spell.value = data.spell
            command.value = data.command
          }).catch(err => {
            spell.value = ''
            command.value = ''
            console.log(err)
            int_id = interval()
          })
        }, 200)
      }
      int_id = interval()
      watchEffect(()=>{
        if(spell.value) {
          console.log(int_id)
          console.log(spell.value,command.value)
          console.log(`command changed`)
          setTimeout(()=>{
            axios.post('http://localhost:8000/chant-spell').then(res => {
              commandResult.value = res.data
              console.log(res)
              console.log(spell.value,command.value)

              setTimeout(() => {
                int_id = interval()
              }, 2000);
            }).catch(err => {
              console.log(err)
            });
            // spell.value = ''
            // command.value = ''
          },2000)
        }
      })
    })
    return { spell, command, commandResult }
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
</style>
