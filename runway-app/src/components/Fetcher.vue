<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useFetch } from '@/hooks/useFetch';

export default defineComponent({
    name: 'Fetcher',
    data() {
        return {
            publicFetchResult: ref<string | null>(''),
            publicFetchHasError: ref(false),
            publicFetchErrorMessage: ref<string | null>(''),
            privateFetchResult: ref<string | null>(''),
            privateFetchHasError: ref(false),
            privateFetchErrorMessage: ref<string | null>(''),
        }
    },
    async beforeMount() {
        const privFetch = await useFetch<string>('http://localhost:5000/api/test/private');
        this.privateFetchHasError = privFetch.hasError.value;
        this.privateFetchResult = privFetch.data.value;
        this.privateFetchErrorMessage = privFetch.errorMessage.value;
    }
});
</script>

<template>
    <div>
        <strong>Private Fetch</strong><br/>
        <p v-if="privateFetchHasError">{{ privateFetchErrorMessage }}</p>
        <pre v-if="privateFetchResult">{{ privateFetchResult }}</pre>
    </div>
</template>
  