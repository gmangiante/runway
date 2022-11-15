<script setup lang="ts">
// App-wide navbar
// Includes menus, logged-in info, notification bell, login button
// Subscribes to SSE for model fit events
import { ref, computed } from 'vue';
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { MDBNavbar, MDBNavbarBrand, MDBBadge, MDBNavbarToggler, MDBCollapse, MDBNavbarNav, MDBNavbarItem, MDBBtn, MDBIcon, MDBToast } from 'mdb-vue-ui-kit';

const navbarCollapsed = ref(false);
const { loginWithRedirect, user, isAuthenticated, logout } = $(useAuth0())

function doLogin() {
  loginWithRedirect({ appState: { target: window.location.pathname } })
}

function doLogout() {
  logout();
}



const evtSource = new EventSource(`http://localhost:5000/events?channel=model_fit`, { withCredentials: true } )

evtSource.addEventListener("complete", (event) => {
    const event_json = JSON.parse(event.data)
    if (event_json['created_by'] == user.email) {
      toastVals.value.model_id = event_json['model_id']
      toastVals.value.model_name = event_json['name']
      toastVals.value.train_score = event_json['train_score']
      toastVals.value.val_score = event_json['val_score']
      unreadNotifications.value.push(toastVals.value)
      toastVals.value.show = true
    }
})

interface Notification {
  show: boolean
  model_id: number
  model_name: string
  train_score: number
  val_score: number
}

const toastVals = ref<Notification>({show: false, model_id: 0, model_name: '', train_score: 0, val_score: 0})
const unreadNotifications = ref([] as Notification[])
const unreadNotificationCount = computed(() => unreadNotifications.value.length)
const showUnreads = ref(false)

const doShowHideUnreads = () => {
  showUnreads.value = !showUnreads.value
  if (!showUnreads.value) unreadNotifications.value = [] as Notification[]
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
          <MDBIcon icon="bell" icon-style="fas" size="lg" class="me-2" @click="doShowHideUnreads()" style="cursor: pointer" />
          <MDBBadge color="primary" pill notification class="translate-middle p-1 mt-2" v-if="unreadNotificationCount > 0">{{ unreadNotificationCount }}</MDBBadge>
          <MDBToast
            v-model="toastVals.show"
            id="fitCompleteToast"
            position="bottom-right"
            width="350px"
            toast="primary"
            :autohide="true" stacking appendToBody :delay="2000">
            <template #title> <RouterLink :to="'/models/' + toastVals.model_id">{{ toastVals.model_name }}</RouterLink> </template>
            <template #small> Fit complete </template>
            train: {{ toastVals.train_score}}, val: {{ toastVals.val_score }}
        </MDBToast>
        <MDBToast v-for="unread in unreadNotifications"
          v-model="showUnreads"
          id="unreadToast"
          position="top-right"
          width="350px"
          toast="primary"
          stacking appendToBody :autohide="false" @hide="unreadNotifications = [] as Notification[]">
          <template #title> <RouterLink :to="'/models/' + unread.model_id">{{ unread.model_name }}</RouterLink> </template>
            <template #small> Fit complete </template>
            train: {{ unread.train_score}}, val: {{ unread.val_score }}
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