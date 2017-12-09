import axios from '@/main'
import { getToken } from '@/util/auth'

export function checkAuth () {
  let localToken = getToken()
  axios.defaults.auth = {
    username: localToken,
    password: localToken
  }
  if (localToken) {
    return true
  } else {
    return false
  }
}
