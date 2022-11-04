// https://github.com/auth0/auth0-vue/issues/99#issuecomment-1104638005

import type { Auth0VueClient } from "@auth0/auth0-vue";
import type { Ref } from "vue";
import { ref } from "vue";

export const client: Ref<Auth0VueClient | undefined> = ref<Auth0VueClient>();

export function exposeAuth0() {
  return {
    install(app: {
      config: { globalProperties: { [x: string]: Auth0VueClient } };
    }) {
      client.value = app.config.globalProperties["$auth0"];
    },
  };
}