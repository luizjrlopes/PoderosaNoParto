import axios from 'axios';
var base = ("http://localhost:3002")
const api = axios.create({
  // baseURL: process.env.REACT_APP_API_URL
  baseURL: base
});

export default api;