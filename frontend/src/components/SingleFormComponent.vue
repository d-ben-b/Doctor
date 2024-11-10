<template>
  <div class="form-container">
    <div class="header">
      <div class="avatar">大頭</div>
      <div class="title">專責醫師平台 - 表單一</div>
      <div class="actions">
        <button class="button remind">提醒</button>
        <button class="button logout">登出</button>
      </div>
    </div>
    <div class="content">
      表單1內容
    </div>
    <button class="submit-button">送出</button>
    <p>Ps: 表單內容填寫處</p>
  </div>
</template>

<script>
export default {
  name: 'SingleFormComponent'
};
</script>

<style scoped>
.form-container {
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
  padding: 10px;
  border: 1px solid #000;
}
.submit-button {
  margin-top: 20px;
  padding: 10px;
  background-color: #1E90FF;
  color: #fff;
  border: none;
  cursor: pointer;
}
p {
  color: #6A0DAD;
}
</style>
  </script>
  
  <style scoped>
  .form-container {
    border: 1px solid #000;
    padding: 20px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .title {
    font-size: 24px;
  }
  .actions .button {
    margin-left: 10px;
  }
  .content {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #000;
  }
  .submit-button {
    margin-top: 20px;
    padding: 10px;
  }
  p {
    color: #6A0DAD;
  }
  </style>