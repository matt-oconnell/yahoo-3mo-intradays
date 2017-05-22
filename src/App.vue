<template>
  <div id="app">
    <table style="width:100%">
        <thead>
            <tr>
                <th>Date</th>
                <th>Close</th>
                <th>Volume</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="el in collection">
                <td>{{ el.date }}</td>
                <td>{{ el.close }}</td>
                <td>{{ el.volume }}</td>
            </tr>
        </tbody>
    </table>
    <button type="button" name="button" @click="req">Button</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      msg: 'stuff',
      collection: [],
    }
  },
  methods: {
    req() {
      const ticker = 'AAPL';
      axios.get(`http://127.0.0.1:5000/ticker/${ticker}`)
      .then(response => {
        this.collection = response.data;
      })
      .catch(e => {
        this.errors.push(e);
      })
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
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
