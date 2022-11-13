<script setup lang="ts">
import { ref } from 'vue';
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { MDBNavbar, MDBNavbarBrand, MDBNavbarToggler, MDBCollapse, MDBNavbarNav, MDBNavbarItem, MDBBtn, MDBIcon, MDBToast } from 'mdb-vue-ui-kit';

const navbarCollapsed = ref(false);
const { loginWithRedirect, user, isAuthenticated, logout } = $(useAuth0())

function doLogin() {
  loginWithRedirect({ appState: { target: window.location.pathname } })
}

function doLogout() {
  logout();
}


const evtSource = new EventSource("//localhost:5000/events?channel=model_fit", { withCredentials: true } )

evtSource.addEventListener("complete", (event) => {
    const event_json = JSON.parse(event.data)
    if (event_json['created_by'] == user.email) {
      toastVals.value.model_name = event_json['name']
      toastVals.value.train_score = event_json['train_score']
      toastVals.value.val_score = event_json['val_score']
      showToast.value = true
    }
})

const toastVals = ref({show: false, model_name: '', train_score: 0, val_score: 0})
const showToast = ref(false)

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
          <MDBIcon icon="bell" icon-style="far" size="lg" class="me-2" />
          <MDBToast
            v-model="showToast"
            :position="'top-right'"
            width="350px"
            toast="primary"
            autohide stacking appendToBody :delay="2000"
        >
            <template #title> {{ toastVals.model_name }} </template>
            <template #small> Fit complete </template>
            train: {{ toastVals.train_score}}, val: {{ toastVals.val_score }}
        </MDBToast>
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