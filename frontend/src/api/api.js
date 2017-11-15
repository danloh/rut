import axios from 'axios'

let base = '/api'

axios.defaults.auth = {
  username: '',
  password: ''
}

const request = (url, options = {}, method = 'get') => {
  let key = ~['delete', 'get', 'head'].indexOf(method) ? 'params' : 'data'
  return axios(Object.assign({'url': url, 'method': method, 'validateStatus': false}, {[key]: options})).then(
        res => res)
}

const register = data => {
  return request(`${base}/register`, data, 'post')
}

const login = () => {
  return request(`${base}/login`)
}

const authUser = params => {
  return request('http://127.0.0.1:5000/api/user', params)  // why cannot be frontend url?
}

const auth = (servername, params) => {
  return request(`${base}/auth/${servername}`, params)
}

const getRuts = params => {
  return request(`${base}/ruts`, params)
}

const getRut = (rutid, params) => {
  return request(`${base}/rut/${rutid}`, params)
}

const getItem = (itemid, params) => {
  return request(`${base}/item/${itemid}`, params)
}

const getClips = params => {
  return request(`${base}/clips`, params)
}

const getDemands = params => {
  return request(`${base}/demands`, params)
}

export {
  axios,
  register,
  login,
  auth,
  authUser,
  getRuts,
  getRut,
  getItem,
  getClips,
  getDemands
}
