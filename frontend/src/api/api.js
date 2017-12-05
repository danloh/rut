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

const fetchCurrentUser = params => {
  return request(`${base}/currentuser`, params)
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

const fetchChallengeItems = params => {   // get some working on items to challenge page
  return request(`${base}/challengeitems`, params)
}

const fetchProfileRuts = (action, userid, params) => {  // act: created, challenge, star
  return request(`${base}/${userid}/${action}/ruts`, params)
}

const fetchRut = (rutid, params) => { // !!
  return request(`${base}/rut/${rutid}`, params)
}
// check if user star or challenge a rut
const checkSC = (rutid, action, params) => {
  return request(`${base}/check${action}/rut/${rutid}`, params)
}
// tag star or challenge a rut
const scRut = (action, rutid, params) => {
  return request(`${base}/${action}/rut/${rutid}`, params)
}

// edit rut
const editRut = (rutid, params) => {
  return request(`${base}/editrut/${rutid}`, params, 'post')
}

const fetchTag = (tagid, params) => { // !!
  return request(`${base}/tag/${tagid}`, params)
}

const fetchItem = (itemid, params) => {
  return request(`${base}/item/${itemid}`, params)
}

const fetchProfileItems = (flag, userid, params) => {
  return request(`${base}/${userid}/${flag}/items`, params)
}

const checkFlag = (itemid, params) => {
  return request(`${base}/checkflag/item/${itemid}`, params)
}

const flagItem = (flag, itemid, params) => {
  return request(`${base}/flag${flag}/item/${itemid}`, params)
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
  fetchCurrentUser,
  fetchUser,
  fetchRuts,
  fetchChallengeRut,
  fetchChallengeItems,
  fetchProfileRuts,
  fetchRut,
  checkSC,
  scRut,
  editRut,
  fetchTag,
  fetchItem,
  checkFlag,
  flagItem,
  fetchProfileItems,
  fetchClips,
  fetchDemands,
  newClip,
  newDemand
}
