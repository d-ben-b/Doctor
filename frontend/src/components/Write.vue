<!-- @format -->

<template>
  <div class="form-container">
    <div class="content">表單1內容</div>
    <button class="submit-button" @click="submitForm">送出</button>
  </div>
</template>

<script>
  export default {
    name: "WriteNew",
    methods: {
      submitForm() {
        // 導航到首頁
        this.$emit("submit-form");
      },
    },
  };
</script>

<style scoped>
  .form-container {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
    background-color: #f9f9f9;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  .avatar {
    width: 50px;
    height: 50px;
    background-color: #000;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-right: 10px;
  }

  .title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
  }

  .actions .button {
    margin-left: 10px;
  }

  .actions .remind,
  .actions .logout {
    padding: 10px;
    color: #fff;
    border: none;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;
    transition: background-color 0.3s;
  }

  .actions .remind {
    background-color: #ffa500;
  }

  .actions .remind:hover {
    background-color: #ff9500;
  }

  .actions .logout {
    background-color: #ff4500;
  }

  .actions .logout:hover {
    background-color: #e03e00;
  }

  .content {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #fff;
    font-size: 18px;
    color: #333;
    text-align: left;
  }

  .submit-button {
    margin-top: 20px;
    padding: 12px 20px;
    background-color: #1e90ff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s;
  }

  .submit-button:hover {
    background-color: #007acc;
  }

  p {
    color: #6a0dad;
  }
</style>
