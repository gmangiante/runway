<script setup lang="ts">
import { ref } from 'vue';
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { MDBNavbar, MDBNavbarBrand, MDBNavbarToggler, MDBCollapse, MDBNavbarNav, MDBNavbarItem, MDBBtn } from 'mdb-vue-ui-kit';

const navbarCollapsed = ref(false);
const { loginWithRedirect, user, isAuthenticated, logout } = $(useAuth0())

function doLogin() {
  loginWithRedirect({ appState: { target: window.location.pathname } })
}

function doLogout() {
  logout();
}

</script>

<template>
  <MDBNavbar expand="lg" dark bg="dark" container position="top">
    <MDBNavbarBrand href="/">runway</MDBNavbarBrand>
    <MDBNavbarToggler
      @click="navbarCollapsed = !navbarCollapsed"
      target="#navbarSupportedContent"
    ></MDBNavbarToggler>
    <MDBCollapse v-model="navbarCollapsed" id="navbarSupportedContent">
      <MDBNavbarNav class="mb-2 mb-lg-0">
        <MDBNavbarItem to="/" class="mt-1" :active="$route.name == 'home'">Home</MDBNavbarItem>
        <MDBNavbarItem to="/datasets" class="mt-1" :active="$route.path.startsWith('/datasets')">Datasets</MDBNavbarItem>
        <MDBNavbarItem to="/models" class="mt-1" :active="$route.path.startsWith('/models')">Models</MDBNavbarItem>
      </MDBNavbarNav>
      <MDBNavbarNav id="navbar-right" class="mt-1">
        <small class="navbar-text mt-1 me-5 text-muted">&copy; 2022 Gabriel Mangiante</small>
        <template v-if="isAuthenticated">
          <div>
          <img
            src="https://avatars.githubusercontent.com/u/3937358?s=120&v=4"
            class="rounded-circle m-2"
            height="30"
            width="30"
            alt=""
            loading="lazy"
          />
          <span class="navbar-text mt-1" id="user-name">{{ user.name }}</span>
        </div>
          <MDBBtn color="primary" @click="doLogout()">Log Out</MDBBtn>
        </template>
        <template v-else>
            <MDBBtn color="primary" @click="doLogin()">Log In</MDBBtn>
        </template>
      </MDBNavbarNav>
    </MDBCollapse>
  </MDBNavbar>
</template>

<style>
#navbar-right {
    margin-right: 0px !important;
}
#user-name {
    margin-right: 10px;
}
</style>