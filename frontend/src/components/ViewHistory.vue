<!-- @format -->

<template>
  <div class="multi-form-container">
    <div class="content">
      <div class="input-group" v-for="input in inputFields" :key="input">
        {{ input }}
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "MultiInputFormComponent",
    data() {
      return {
        inputFields: [
          "人員 A",
          "人員 B",
          "人員 C",
          "人員 D",
          "人員 A1",
          "人員 B1",
          "人員 C1",
          "人員 D1",
          "人員 A2",
          "人員 B2",
          "人員 C2",
          "人員 D2",
        ],
      };
    },
  };
</script>

<style scoped>
  .multi-form-container {
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 8px;
    max-width: 600px;
    margin: 0 auto;
    background-color: #f9f9f9;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  }

  .content {
    margin-top: 20px;
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* 四列布局 */
    gap: 10px;
  }

  .input-group {
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #ffffff;
    text-align: center;
    font-size: 16px;
    color: #333;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .input-group:hover {
    transform: translateY(-3px);
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
  }

  p {
    color: #6a0dad;
  }
</style>
