<!-- @format -->

<template>
  <div class="container">
    <div class="work-list">
      <div class="work-item" v-for="(work, index) in workList" :key="index">
        <p>{{ work.work_place }}</p>
        <ul>
          <li
            class="name"
            v-for="(work_name, idx) in work.work_names"
            :key="idx">
            ○ {{ work_name }}
          </li>
        </ul>
      </div>
    </div>
    <div class="login-form">
      <input type="text" placeholder="使用者名稱" />
      <input type="password" placeholder="密碼" />
      <button class="login-button" @click="toggleLogin">登入</button>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["workList"],

    methods: {
      toggleLogin() {
        this.$emit("toggle-login");
      },
    },
  };
</script>

<style scoped>
  .container {
    display: flex;
    flex-direction: row; /* 主容器水平排列 */
    justify-content: space-between;
    padding: 20px;
    border: 2px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .work-list {
    width: 60%; /* 左側區域寬度 */
    display: flex;
    flex-direction: column; /* 垂直排列每個診室 */
    padding: 15px;
    font-size: 18px;
    border-right: 1px solid #ccc; /* 分隔線 */
  }

  .work-item {
    margin-bottom: 15px; /* 診室之間的間距 */
    font-weight: bold;
    color: #333;
  }

  .name {
    margin-left: 20px;
    font-size: 16px;
    color: #666;
  }

  .login-form {
    width: 35%; /* 右側表單寬度 */
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
