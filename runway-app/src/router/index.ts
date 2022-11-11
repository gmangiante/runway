import { authGuard } from "@auth0/auth0-vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("../views/HomeView.vue"),
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/datasets",
      name: "datasets",
      component: () => import("../views/DatasetsView.vue"),
    },
    {
      path: "/datasets/create",
      name: "createDataset",
      component: () => import("../views/CreateDatasetView.vue"),
      beforeEnter: authGuard
    },
    {
      path: "/datasets/:id",
      name: "datasetDetail",
      component: () => import("../views/DatasetDetailView.vue"),
      props: true
    },
    {
      path: "/models",
      name: "models",
      component: () => import("../views/ModelsView.vue"),
    },
    {
      path: "/models/create/:dataset_id",
      name: "createModel",
      component: () => import("../views/CreateModelView.vue"),
      props: true,
      beforeEnter: authGuard
    },
    {
      path: "/models/:id",
      name: "modelDetail",
      component: () => import("../views/ModelDetailView.vue"),
      props: true
    }
  ],
});

export default router;
