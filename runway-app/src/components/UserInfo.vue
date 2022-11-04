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
        <pre>
            <code>{{ user.name }}</code>
        </pre>
    </div>
</template>