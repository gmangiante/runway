<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LogoutButton',
  methods: {
    logout() {
      this.$auth0.logout({ returnTo: window.location.origin });
    }
  }
});
</script>

<template>
  <div>
    <button @click="logout">Log out</button>
  </div>
</template>
  