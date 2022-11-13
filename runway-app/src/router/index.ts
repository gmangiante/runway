import { authGuard } from "@auth0/auth0-vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("../components/Home.vue"),
    },
    {
      path: "/datasets",
      name: "datasetList",
      component: () => import("../components/dataset/List.vue"),
    },
    {
      path: "/datasets/:id",
      name: "datasetDetail",
      component: () => import("../components/dataset/Detail.vue"),
      props: true
    },
    {
      path: "/datasets/create",
      name: "createDataset",
      component: () => import("../components/dataset/Create.vue"),
      beforeEnter: authGuard
    },
    {
      path: "/models",
      name: "modelList",
      component: () => import("../components/model/List.vue"),
    },
    {
      path: "/models/:id",
      name: "modelDetail",
      component: () => import("../components/model/Detail.vue"),
      props: true
    },
    {
      path: "/models/create/:dataset_id",
      name: "createModel",
      component: () => import("../components/model/Create.vue"),
      props: true,
      beforeEnter: authGuard
    }
  ]
});

export default router;
