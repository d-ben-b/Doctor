<!-- @format -->

<template>
  <div class="form-item">
    <div class="form-name">{{ form.name }}</div>
    <div class="form-description">{{ form.description }}</div>
  </div>
</template>

<script>
  export default {
    props: ["form"],
  };
</script>

<style scoped>
  .form-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .form-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }

  .form-name {
    font-size: 22px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }

  .form-description {
    font-size: 16px;
    color: #666;
    line-height: 1.5;
    text-align: center;
  }
</style>
