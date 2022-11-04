<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'UserInfo',
    data() {
        return {
            user: this.$auth0.user
        }
    }
});
</script>

<template>
    <div>
        <h2>User Profile</h2>
        <pre>
            <code>{{ user }}</code>
        </pre>
    </div>
</template>