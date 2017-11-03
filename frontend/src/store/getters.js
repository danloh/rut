export default {
  // ids of the items that should be currently displayed based on
  // current list type and current pagination
  activeUser (state) {
    const { user } = state

    if (!user) {
      return null
    }
    return user
  }
}
