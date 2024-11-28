<!-- @format -->

<template>
  <div class="container">
    <!-- 工作清單 -->
    <div class="work-list">
      <div
        class="work-item"
        v-for="(announcement, index) in announcementList"
        :key="index">
        <p>{{ announcement.work_place }}</p>
        <ul>
          <li
            class="name"
            v-for="(announcement_name, idx) in announcement.work_names"
            :key="idx">
            {{ announcement_name }}
          </li>
        </ul>
      </div>
    </div>

    <!-- 登入表單 -->
    <div class="login-form">
      <h2>登入</h2>
      <p class="error-message" v-if="errorMessage">{{ errorMessage }}</p>
      <input
        type="text"
        placeholder="使用者名稱"
        v-model="username"
        @keydown="clearError" />
      <input
        type="password"
        placeholder="密碼"
        v-model="password"
        @keydown="clearError" />
      <button class="login-button" @click="handleLogin">登入</button>
    </div>
  </div>
</template>

<script>
  import { ReadAPI } from "@/composables/useNavigation";

  export default {
    data() {
      return {
        announcementList: [],
        username: "",
        password: "",
        errorMessage: "",
      };
    },
    methods: {
      async handleLogin() {
        if (!this.username || !this.password) {
          this.errorMessage = "請輸入使用者名稱和密碼";
          return;
        }

        const loginData = {
          username: this.username,
          password: this.password,
        };

        try {
          // 等待 ReadAPI 返回的資料，並賦值給 this.categories
          const response = await ReadAPI("/login", "POST", loginData);

          if (response.token) {
            console.log("登入成功", response);
            // 儲存 token，供後續 API 調用使用
            localStorage.setItem("token", response.token);
            localStorage.setItem("id", response.id);
            this.$router.push("/cases");
          } else {
            this.errorMessage = "登入失敗，請確認帳號密碼";
          }
        } catch (error) {
          console.error("登入失敗", error);
          if (error.response && error.response.status === 401) {
            this.errorMessage = "帳號或密碼錯誤";
          } else {
            this.errorMessage = "伺服器錯誤，請稍後再試";
          }
        }
      },
      async fetchAnnouncementList() {
        try {
          // 等待 ReadAPI 返回的資料，並賦值給 this.categories
          const response = await ReadAPI("/announcementList", "GET");
          this.announcementList = response;
        } catch (error) {
          console.error("無法加載數據", error);
          this.errorMessage = "無法加載工作清單，請稍後重試。";
        }
      },
      clearError() {
        this.errorMessage = "";
      },
    },
    async mounted() {
      this.fetchAnnouncementList();
    },
  };
</script>

<style scoped>
  /* 與原樣式相同，無需更改 */
  .container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 20px;
    border: 2px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  .work-list {
    width: 60%;
    display: flex;
    flex-direction: column;
    padding: 15px;
    font-size: 18px;
    border-right: 1px solid #ccc;
  }
  .work-item {
    margin-bottom: 15px;
    font-weight: bold;
    color: #333;
  }
  .name {
    margin-left: 20px;
    font-size: 16px;
    color: #666;
  }
  .login-form {
    width: 35%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 20px;
    background-color: #ffffff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  h2 {
    margin-bottom: 20px;
    font-size: 24px;
    color: #333;
  }
  .error-message {
    color: red;
    font-size: 14px;
    margin-bottom: 15px;
  }
  input[type="text"],
  input[type="password"] {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    color: #333;
  }
  input[type="text"]::placeholder,
  input[type="password"]::placeholder {
    color: #999;
  }
  .login-button {
    padding: 10px;
    border: none;
    background-color: #007bff;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .login-button:hover {
    background-color: #0056b3;
  }
</style>
