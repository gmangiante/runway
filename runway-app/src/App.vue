<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import HelloWorld from "./components/HelloWorld.vue";
import LoginButton from './components/LoginButton.vue';
import LogoutButton from './components/LogoutButton.vue';
import UserInfo from './components/UserInfo.vue';
import { useAuth0 } from "@auth0/auth0-vue";
import Fetcher from './components/Fetcher.vue';
const auth0Client = useAuth0();
function vnbItemClicked(text: string) {
    if (text === 'Login') {
      auth0Client.loginWithRedirect();
    }
  }

</script>

<template>
  <header>
    
  </header>
  <div class="wrapper">
    <RouterView />
  </div>  
</template>

<style scoped>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");
header {
  line-height: 1.5;
  max-height: 15vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  .wrapper {
    display: flex;
    float: left;
    place-items: flex-start;
    flex-wrap: wrap;
    width: 100vw;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
