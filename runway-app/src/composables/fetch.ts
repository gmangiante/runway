// https://javascript.plainenglish.io/create-a-basic-usefetch-hook-in-vue-b3ff113872d7
// https://vuejs.org/guide/reusability/composables.html#async-state-example

import { isRef, reactive, toRefs, ref, unref, watchEffect } from 'vue';
import type { UnwrapRef } from 'vue'
import { client } from './nonComponentAuth0';


export const useFetch = async <T>(
    url: string,
    options: RequestInit = {} as RequestInit ) => {

    const state = reactive<FetchState<T>>({
        isLoading: true,
        hasError: false,
        errorMessage: '',
        data: null,
        blob: null
    })

    const doFetch = async() =>
    {
        state.isLoading = true
        state.hasError = false
        state.errorMessage = ''
        state.data = null

        const urlValue = unref(url)
        const optionsValue = unref(options)

        try {
            const cli = unref(client);
            if (!cli) throw new Error('Unable to acquire Auth0 client')

            if (cli.isAuthenticated) {
                const token = await cli.getAccessTokenSilently()
                const headers = optionsValue.headers ? new Headers(optionsValue.headers) : new Headers()
                headers.set("Authorization", `Bearer ${token}`)
                optionsValue.headers = headers
                optionsValue.credentials = "include"
            }
            
            const response = await fetch(urlValue, optionsValue)

            if (!response.ok) {
                throw new Error(response.statusText);               
            }

            if (response.headers.get('Content-Type')?.includes('json'))
                state.data = await response.json()
            else
                state.blob = await response.blob()
        }
        catch (error: unknown) {
            state.hasError = true
            state.errorMessage = (error as Error).message
        }
        finally {
            state.isLoading = false
        }
        console.log(state)
    }

    if (isRef(url) || isRef(options))
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
    blob: Blob | null
}