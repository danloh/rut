import axios from '@/main'

let base = '/api'
const request = (url, options = {}, method = 'get') => {
  let key = ~['delete', 'get', 'head'].indexOf(method) ? 'params' : 'data'
  return axios(Object.assign({'url': url, 'method': method, 'validateStatus': false}, {[key]: options}))
  .then(res => res)
}

const register = data => {
  return request(`${base}/register`, data, 'post')
}

const login = () => {
  return request(`${base}/login`)
}

const authUser = params => {
  return request(`${base}/user`, params)  // why cannot be frontend url?
}

const auth = (servername, params) => {
  return request(`${base}/auth/${servername}`, params)
}

const fetchRuts = params => {
  return request(`${base}/ruts`, params)
}

const fetchChallengeRuts = params => {
  return request(`${base}/challengeruts`, params)
}

const fetchRut = (rutid, params) => { // !!
  return request(`${base}/rut/${rutid}`, params)
}

const fetchTag = (tagid, params) => { // !!
  return request(`${base}/tag/${tagid}`, params)
}

const getItem = (itemid, params) => {
  return request(`${base}/item/${itemid}`, params)
}

const fetchClips = params => {
  return request(`${base}/clips`, params)
}

const newClip = params => {
  return request(`${base}/newclip`, params, 'post')
}

const fetchDemands = (params) => {
  return request(`${base}/demands`, params)
}

const newDemand = params => {
  return request(`${base}/newdemand`, params, 'post')
}

export {
  axios,
  register,
  login,
  auth,
  authUser,
  fetchRuts,
  fetchChallengeRuts,
  fetchRut,
  fetchTag,
  getItem,
  fetchClips,
  fetchDemands,
  newClip,
  newDemand
}
