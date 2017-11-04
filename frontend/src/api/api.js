import axios from 'axios'

let base = '/api'

const request = (url, options = {}, method = 'get') => {
  let key = ~['delete', 'get', 'head'].indexOf(method) ? 'params' : 'data'
  return axios(Object.assign({'url': url, 'method': method, 'validateStatus': false}, {[key]: options})).then(
        res => res)
}

const authUser = params => {
  return request(`${base}/user`, params)
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

export {
  authUser,
  getRuts,
  getRut,
  getItem
}
