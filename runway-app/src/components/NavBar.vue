<script setup lang="ts">
import { ref } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { MDBNavbar, MDBNavbarBrand, MDBNavbarToggler, MDBCollapse, MDBNavbarNav, MDBNavbarItem, MDBBtn } from 'mdb-vue-ui-kit';

const navbarCollapsed = ref(false);
const { loginWithRedirect, user, isAuthenticated, logout } = useAuth0();

</script>

<template>
<MDBNavbar expand="lg" dark bg="dark" container>
    <MDBNavbarBrand href="#">runway</MDBNavbarBrand>
    <MDBNavbarToggler
      @click="navbarCollapsed = !navbarCollapsed"
      target="#navbarSupportedContent"
    ></MDBNavbarToggler>
    <MDBCollapse v-model="navbarCollapsed" id="navbarSupportedContent">
      <MDBNavbarNav class="mb-2 mb-lg-0">
        <MDBNavbarItem to="/" class="mt-1">
          Home
        </MDBNavbarItem>
        <template v-if="isAuthenticated">
            <MDBNavbarItem to="/datasets" class="mt-1">Datasets</MDBNavbarItem>
            <MDBNavbarItem to="/chart" class="mt-1">Chart</MDBNavbarItem>
            <MDBNavbarItem to="/upload" class="mt-1">Upload</MDBNavbarItem>
        </template>
      </MDBNavbarNav>
      <MDBNavbarNav id="navbar-right" class="mt-1">
        <template v-if="isAuthenticated">
          <span class="navbar-text" id="user-name">{{ user.name }}</span>
          <MDBBtn color="primary" @click="logout()">Log Out</MDBBtn>
        </template>
        <template v-else>
            <MDBBtn color="primary" @click="loginWithRedirect()">Log In</MDBBtn>
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