import { createApp } from "vue";
import { createPinia } from "pinia";
import { createAuth0 } from '@auth0/auth0-vue';
import { useNonComponentAuth0 } from "./composables/nonComponentAuth0";

import App from "./App.vue";
import router from "./router";

import 'mdb-vue-ui-kit/css/mdb.min.css';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.use(
    createAuth0({
      domain: "dev-c3pt87w5gyl1mcox.us.auth0.com",
      client_id: "yoKIWRYGdrKqNu7BxswWqSuC9JpIUydE",
      redirect_uri: window.location.origin,
      audience: "https://runway/api"
    })
  );

app.use(useNonComponentAuth0());

app.mount("#app");
