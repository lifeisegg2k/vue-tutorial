/** @format */

import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import JobsView from "@/views/JobsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      nmae: "Home",
      component: HomeView,
    },
    {
      path: "/jobs",
      nmae: "Jobs",
      component: JobsView,
    },
  ],
});

export default router;
