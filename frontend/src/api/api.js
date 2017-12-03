import axios from '@/main'

let base = '/api'
const request = (url, options = {}, method = 'get') => {
  let key = ~['delete', 'get', 'head'].indexOf(method) ? 'params' : 'data' // bitwise NOT: ~N -> -(N+1)
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

const fetchUser = (id, params) => {
  return request(`${base}/user/${id}`, params)
}

const fetchRuts = params => {
  return request(`${base}/ruts`, params)
}

const fetchChallengeRut = params => {
  return request(`${base}/challengerut`, params)
}

const fetchProfileRuts = (action, params) => {  // act: created, challenge, star
  return request(`${base}/${action}/ruts`, params)
}

const fetchRut = (rutid, params) => { // !!
  return request(`${base}/rut/${rutid}`, params)
}

const fetchTag = (tagid, params) => { // !!
  return request(`${base}/tag/${tagid}`, params)
}

const fetchItem = (itemid, params) => {
  return request(`${base}/item/${itemid}`, params)
}

const fetchItems = (flag, params) => {
  return request(`${base}/items/${flag}`, params)
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
  fetchUser,
  fetchRuts,
  fetchChallengeRut,
  fetchProfileRuts,
  fetchRut,
  fetchTag,
  fetchItem,
  fetchItems,
  fetchClips,
  fetchDemands,
  newClip,
  newDemand
}
