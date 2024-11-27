/** @format */

import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import TaskDetails from "@/views/TaskDetails.vue";
import CaseManagement from "@/views/CaseManagement.vue";
import Edit from "@/views/Edit.vue";

const routes = [
  { path: "/login", name: "Login", component: Login },
  { path: "/:pathMatch(.*)*", redirect: "/login" }, // 未知路徑重定向
  { path: "/task-details", name: "TaskDetails", component: TaskDetails },
  { path: "/cases", name: "cases", component: CaseManagement },
  { path: "/edit", name: "edit", component: Edit },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
