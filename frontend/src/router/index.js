/** @format */

import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Dashboard from "@/views/Dashboard.vue";
import TaskDetails from "@/views/TaskDetails.vue";

const routes = [
  { path: "/login", name: "Login", component: Login },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
  { path: "/:pathMatch(.*)*", redirect: "/login" }, // 未知路徑重定向
  { path: "/task-details", name: "TaskDetails", component: TaskDetails },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;