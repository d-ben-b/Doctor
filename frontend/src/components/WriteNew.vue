<!-- @format -->

<template>
  <div class="form-item">
    <div class="write-new" @click="show(0)">填寫新表單</div>
    <div class="history" @click="show(1)">填寫紀錄</div>
    <write v-if="write == 0" @submit-form="submitForm" />
    <history v-else />
  </div>
</template>

<script>
  import Write from "./Write.vue";
  import History from "./ViewHistory.vue";

  export default {
    data() {
      return {
        write: 0,
      };
    },
    methods: {
      show(type) {
        this.write = type;
      },
      submitForm() {
        // 重置狀態以模擬返回首頁
        this.$emit("submit");
      },
    },
    components: {
      write: Write,
      history: History,
    },
  };
</script>

<style scoped>
  .form-item {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 15px;
    background-color: #f9f9f9;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }

  .write-new,
  .history {
    cursor: pointer;
    padding: 10px;
    margin: 10px 0;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    color: #007bff;
    border: 1px solid #007bff;
    border-radius: 5px;
    background-color: #fff;
    transition: background-color 0.3s, color 0.3s;
  }

  .write-new:hover,
  .history:hover {
    background-color: #007bff;
    color: #fff;
  }
</style>
