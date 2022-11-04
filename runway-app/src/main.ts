import { createApp } from "vue";
import { createPinia } from "pinia";
import { createAuth0 } from '@auth0/auth0-vue';
import { exposeAuth0 } from "./hooks/exposeAuth";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

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

app.use(exposeAuth0());

app.mount("#app");
