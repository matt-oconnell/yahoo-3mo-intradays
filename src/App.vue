<template>
  <div id="app">
    <input type="text" v-model="ticker">
    <button type="button" name="button" @click="req">Get Last 3 Months</button>
    <br>
    <input type="checkbox" v-model="filterChecked"></input>
    <label>Filter</label>
    <div v-if="filterChecked">
      <input v-model="filters" type="text" placeholder="09:30,10:00,3:30"></input>
    </div>
    <!--<div class="inputs">
      <select>
        <option v-for="time in uniqueTimes" :value="time.timestamp">{{ time.readable }}</option>
      </select>
    </div>-->
    <br>
    <br>
    <table style="width:100%">
      <thead>
        <tr>
          <th>Date</th>
          <th>Low</th>
          <th>High</th>
          <th>Open</th>
          <th>Close</th>
          <th>Volume</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="el in collection">
          <td>{{ el.date }}</td>
          <td>{{ el.low }}</td>
          <td>{{ el.high }}</td>
          <td>{{ el.open }}</td>
          <td>{{ el.close }}</td>
          <td>{{ el.volume }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import _ from 'lodash';

export default {
  data() {
    return {
      msg: 'stuff',
      collection: [],
      ticker: '',
      uniqueTimes: [],
      filterChecked: false,
    }
  },
  methods: {
    req() {
      if (!this.ticker) {
        return;
      }
      axios.get(`${window.location.href}ticker/${this.ticker}`)
      .then(response => {
        this.collection = response.data.collection;
        this.updateUniqueTimes();
      })
      .catch(e => {
        throw new Error(e);
      })
    },
    updateUniqueTimes() {
      const times = this.collection.map(el => {
        return {
          readable: /\s\d\d:\d\d/.exec(el.date)[0].trim(),
          timestamp: el.timestamp,
        }
      });
      this.uniqueTimes = _.uniqBy(times, 'readable');
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

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}

th, td {
  padding: 4px;
}
</style>
