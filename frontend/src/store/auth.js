/** @format */

import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false, // 登入狀態
  }),
  actions: {
    login() {
      this.isAuthenticated = true;
    },
    logout() {
      this.isAuthenticated = false;
      localStorage.removeItem("token"); // 清除 Token（如有使用）
    },
  },
});
