// https://javascript.plainenglish.io/create-a-basic-usefetch-hook-in-vue-b3ff113872d7
import { reactive, toRefs, unref } from 'vue';
import { client } from './exposeAuth';

interface State<T> {
    isLoading: boolean;
    hasError: boolean;
    errorMessage: string;
    data: T | null;
}

export const useFetch = async <T>(
    url: string,
    options?: Record<string, unknown>,
) => {
    const state = reactive<State<T>>({
        isLoading: true,
        hasError: false,
        errorMessage: '',
        data: null,
    });

    const fetchData = async() => {
        state.isLoading = true;

        try {
            const cli = unref(client);

            if (!cli) throw new Error('Unable to acquire Auth0 client');

            const token = await cli.getAccessTokenSilently();
            
            const response = await fetch(url, { headers: {
                Authorization: 'Bearer ' + token
              }});

            if (!response.ok) {
                throw new Error(response.statusText);                
            }

            state.data = await response.json();
        }
        catch (error: unknown) {
            const typedError = error as Error;
            state.hasError = true;
            state.errorMessage = typedError.message;
        }
        finally {
            state.isLoading = false;
        }
    };

    await fetchData();

    return { ...toRefs(state) };
};