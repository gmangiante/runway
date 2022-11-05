// https://javascript.plainenglish.io/create-a-basic-usefetch-hook-in-vue-b3ff113872d7
// https://vuejs.org/guide/reusability/composables.html#async-state-example

import { isRef, reactive, toRefs, unref, watchEffect, computed } from 'vue';
import { client } from './nonComponentAuth0';

export const useFetch = async <T>(
    url: string,
    useAuth: boolean = true,
    options: RequestInit = {} as RequestInit ) => {

    const state = reactive<FetchState<T>>({
        isLoading: true,
        hasError: false,
        errorMessage: '',
        data: null
    })

    const doFetch = async() =>
    {
        state.isLoading = true
        state.hasError = false
        state.errorMessage = ''
        state.data = null

        const urlValue = unref(url)
        const useAuthValue = unref(useAuth)
        const optionsValue = unref(options)

        try {
            if (useAuthValue)
            {
                const cli = unref(client);
                if (!cli) throw new Error('Unable to acquire Auth0 client')
                const token = await cli.getAccessTokenSilently()
                const headers = optionsValue.headers ? new Headers(optionsValue.headers) : new Headers()
                headers.set("Authorization", `Bearer ${token}`)
                optionsValue.headers = headers
            }
            
            const response = await fetch(urlValue, optionsValue)

            if (!response.ok) {
                throw new Error(response.statusText);               
            }

            state.data = await response.json()
        }
        catch (error: unknown) {
            state.hasError = true
            state.errorMessage = (error as Error).message
        }
        finally {
            state.isLoading = false
        }
    }

    if (isRef(url) || isRef(useAuth) || isRef(options))
    {
        watchEffect(doFetch)
    }
    else
    {
        await doFetch()
    }

    return { ...toRefs(state) }
}

export interface FetchState<T> {
    isLoading: boolean
    hasError: boolean
    errorMessage: string
    data: T | null
}