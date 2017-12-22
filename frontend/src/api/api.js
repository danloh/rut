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

const confirm = (token) => {
  return request(`${base}/confirm/${token}`)
}
// change password
const change = (data) => {
  return request(`${base}/changepassword`, data, 'post')
}
// rest password if forget password
const reset = (token, data) => {
  return request(`${base}/reset/${token}`, data, 'post')
}

const login = () => {
  return request(`${base}/login`)
}

// const authUser = params => {
//   return request(`${base}/user`, params)  // why cannot be frontend url?
// }

// const auth = (servername, params) => {
//   return request(`${base}/auth/${servername}`, params)
// }
// get authed user info
const fetchCurrentUser = params => {
  return request(`${base}/currentuser`, params)
}
// get user info
const fetchUser = (id, params) => {
  return request(`${base}/user/${id}`, params)
}
// get follows
const fetchFollows = (userid, follow, params) => {
  return request(`${base}/user/${userid}/${follow}`, params)
}

const editProfile = (params) => {
  return request(`${base}/editprofile`, params, 'post')
}
// check if follow someone
const checkFollowing = (userid, params) => {
  return request(`${base}/checkfollow/${userid}`, params)
}
// fo / unfo someone
const followOne = (action, userid, params) => {
  return request(`${base}/${action}/user/${userid}`, params)
}
// create new rut
const newRut = (params, demandid) => {
  return request(`${base}/create/${demandid}`, params, 'post')
}

const fetchRuts = params => {
  return request(`${base}/ruts`, params)
}
// get one challenge rut
const fetchChallengeRut = params => {
  return request(`${base}/challengerut`, params)
}
// get some working on items to challenge page
const fetchChallengeItems = params => {
  return request(`${base}/challengeitems`, params)
}
// set challenge deadline
const setDeadline = params => {
  return request(`${base}/setdeadline`, params)
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
// edit rut's tags
const editTags = (rutid, params) => {
  return request(`${base}/edittags/${rutid}`, params, 'post')
}
// add item to rut, new or check existing
const addItem = (rutid, params) => {
  return request(`${base}/additemtorut/${rutid}`, params, 'post')
}
// add existing item to rut
const itemToRut = (itemid, rutid, params) => {
  return request(`${base}/item/${itemid}/torut/${rutid}`, params)
}
// check item to add
const checkItem = (rutid, params) => {
  return request(`${base}/checkitemtoadd/${rutid}`, params, 'post')
}
// edit tips
const editTips = (cid, params) => {
  return request(`${base}/edittips/${cid}`, params, 'post')
}

const fetchTag = (tagid, params) => { // !!
  return request(`${base}/tag/${tagid}`, params)
}
// edit tag
const editTag = (tagid, params) => {
  return request(`${base}/edittag/${tagid}`, params, 'post')
}
// check faving tag
const checkFav = (tagid, params) => {
  return request(`${base}/checkfavtag/${tagid}`, params)
}
// fav unfav tag
const favTag = (action, tagid, params) => {
  return request(`${base}/${action}/tag/${tagid}`, params)
}
// get Item
const fetchItem = (itemid, params) => {
  return request(`${base}/item/${itemid}`, params)
}
// edit item
const editItem = (itemid, params) => {
  return request(`${base}/edititem/${itemid}`, params, 'post')
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
// for specific item or user
const fetchIUClips = params => {
  return request(`${base}/iuclips`, params)
}

const newClip = params => {
  return request(`${base}/newclip`, params, 'post')
}
// upvote clip
const upvoteClip = (clipid, params) => {
  return request(`${base}/upvoteclip/${clipid}`, params)
}
// create review
const newReview = (itemid, params) => {
  return request(`${base}/newreview/${itemid}`, params, 'post')
}
// fetch review
const fetchReview = (reviewid, params) => {
  return request(`${base}/review/${reviewid}`, params)
}
// edit review
const editReview = (reviewid, params) => {
  return request(`${base}/editreview/${reviewid}`, params, 'post')
}
// upvote review
const upvoteReview = (reviewid, params) => {
  return request(`${base}/upvotereview/${reviewid}`, params)
}
// get demand list
const fetchDemands = (params) => {
  return request(`${base}/demands`, params)
}
// get specific demand
const fetchDemand = (demandid, params) => {
  return request(`${base}/demand/${demandid}`, params)
}
// submit new demand
const newDemand = params => {
  return request(`${base}/newdemand`, params, 'post')
}
// upvote demand
const upvoteDemand = (demandid, params) => {
  return request(`${base}/upvotedemand/${demandid}`, params)
}
// link a rut to demand as Answer
const rutAsAnswer = (rutid, demandid, params) => {
  return request(`${base}/rut/${rutid}/answerdemand/${demandid}`, params)
}
// post new comment
const newComment = (ref, id, params) => {
  return request(`${base}/comment/${ref}/${id}`, params, 'post')
}
// get comments for a rut
const fetchRutComment = (rutid, params) => {
  return request(`${base}/commentonrut/${rutid}`, params)
}

export {
  axios,
  register,
  confirm,
  change,
  reset,
  login,
  // auth,
  // authUser,
  fetchCurrentUser,
  fetchUser,
  fetchFollows,
  editProfile,
  checkFollowing,
  followOne,
  newRut,
  fetchRuts,
  fetchChallengeRut,
  fetchChallengeItems,
  setDeadline,
  fetchProfileRuts,
  fetchRut,
  checkSC,
  scRut,
  editRut,
  editTags,
  addItem,
  itemToRut,
  checkItem,
  editTips,
  fetchTag,
  editTag,
  checkFav,
  favTag,
  fetchItem,
  checkFlag,
  flagItem,
  editItem,
  fetchProfileItems,
  fetchClips,
  fetchIUClips,
  newReview,
  fetchReview,
  editReview,
  upvoteReview,
  fetchDemands,
  fetchDemand,
  newClip,
  upvoteClip,
  newDemand,
  upvoteDemand,
  rutAsAnswer,
  newComment,
  fetchRutComment
}
