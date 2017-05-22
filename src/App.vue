<template>
  <div id="app">
    <input type="text" v-model="ticker">
    <button type="button" name="button" @click="req">Button</button>
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      msg: 'stuff',
      collection: [],
      ticker: '',
    }
  },
  methods: {
    req() {
      if (!this.ticker) {
        return;
      }
      axios.get(`${window.location.href}ticker/${this.ticker}`)
      .then(response => {
        this.collection = response.data;
      })
      .catch(e => {
        throw new Error(e);
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
