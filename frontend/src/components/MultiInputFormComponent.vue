<template>
    <div class="multi-form-container">
      <div class="header">
        <div class="avatar">大頭</div>
        <div class="title">專責醫師平台 - 表單一</div>
        <div class="actions">
          <button class="button remind">提醒</button>
          <button class="button logout">登出</button>
        </div>
      </div>
      <div class="content">
        <div class="input-group" v-for="input in inputFields" :key="input">
          {{ input }}
        </div>
      </div>
      <p>Ps: 查看填寫記錄。</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MultiInputFormComponent',
    data() {
      return {
        inputFields: ['人員 A', '人員 B', '人員 C', '人員 D', '人員 A!', '人員 B!', '人員 C!', '人員 D!', '人員 A?', '人員 B?', '人員 C?', '人員 D?']
      };
    }
  };
  </script>
  
  <style scoped>
  .multi-form-container {
    border: 1px solid #000;
    padding: 20px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
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
  }
  .actions .button {
    margin-left: 10px;
  }
  .actions .remind {
    background-color: #FFA500;
    color: #fff;
    border: none;
    padding: 10px;
    cursor: pointer;
  }
  .actions .logout {
    background-color: #FF4500;
    color: #fff;
    border: none;
    padding: 10px;
    cursor: pointer;
  }
  .content {
    margin-top: 20px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }
  .input-group {
    padding: 10px;
    border: 1px solid #000;
    text-align: center;
  }
  p {
    color: #6A0DAD;
  }
  </style>