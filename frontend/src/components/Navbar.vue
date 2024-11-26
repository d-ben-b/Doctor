<!-- @format -->

<template>
  <div class="navbar">
    <!-- 標題與導航按鈕 -->
    <img src="/head.png" alt="頭像" v-show="login" @click="resetStates" />
    <h2>專責醫師平台</h2>
    <button class="button remind" v-show="login">提醒</button>
    <button class="button logout" @click="logout" v-show="login">登出</button>
    <hr />
  </div>
</template>

<script>
  import { useRouter } from "vue-router";

  export default {
    name: "Navbar",
    data() {
      return {
        login: true, // 登入狀態
      };
    },
    setup() {
      const router = useRouter();

      // 登出時重置狀態並跳轉至登入頁面
      const logout = () => {
        // 假設清除登入狀態的方法
        router.push("/login"); // 跳轉到登入頁面
      };

      // 重置狀態回到初始視圖
      const resetStates = () => {
        router.push("/cases"); // 假設重置後回到 Dashboard
      };

      return {
        logout,
        resetStates,
      };
    },
  };
</script>

<style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 25px;
    background-color: #f8f9fa;
    border-bottom: 1px solid #ddd;
  }

  img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
  }

  h2 {
    margin: 0;
    flex-grow: 1;
    text-align: center;
    font-size: 24px;
    color: #333;
  }

  .button {
    padding: 8px 12px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .remind {
    background-color: #ffa500;
    color: #fff;
    border: none;
  }

  .remind:hover {
    background-color: #ff9500;
  }

  .logout {
    background-color: #ff4500;
    color: #fff;
    border: none;
  }

  .logout:hover {
    background-color: #e03e00;
  }
</style>
