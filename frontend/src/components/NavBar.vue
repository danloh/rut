<template>
  <div class="menu">
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>                        
          </button>
          <router-link class="navbar-brand" to="/">
            <b style="color:darkorange">Readup.Tips</b>
          </router-link>
        </div>

        <div class="collapse navbar-collapse" id="myNavbar">
          <ul class="nav navbar-nav">
            <li><router-link to="/challenge">
              <b>Challenge</b>
            </router-link></li>
            <li><router-link to="/demand">
              <b>Request</b>
            </router-link></li>
          </ul>

          <ul class="nav navbar-nav navbar-right">
            <li v-if="this.$store.state.user != null">	
              <router-link class="btn btn-success navbar-btn" to="/create">
                <b style="color:white">Create Now</b>
              </router-link>
              <router-link class="btn navbar-btn" :to="{ name: 'Profile' }">
                <img src="#" \
                style="width:24px;height:22px" alt="Profile" class="img-circle" \
                title="#">
              </router-link>
              <button class="btn navbar-btn dropdown-toggle" data-toggle="dropdown">
                <span class="caret"></span>
              </button>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <ul class="dropdown-menu" role="menu">
                <li><router-link :to="{ name: 'Editprofile' }">Edit Profile</router-link></li>
                <li class="divider"></li>
                <li><router-link :to="{ name: 'Logout' }">Logout</router-link></li>
              </ul>
            </li>

            <li v-if="this.$store.state.user == null">
              <router-link class="btn navbar-btn" :to="{ name: 'Connect' }">
                <b style="color:white">Connet</b>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'menu'
}
</script>