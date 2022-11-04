<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'LoginButton',
    methods: {
        login() {
            this.$auth0.loginWithRedirect();
        }
    }
});
</script>

<template>
    <div>
        <button @click="login">Log in</button>
    </div>
</template>
  