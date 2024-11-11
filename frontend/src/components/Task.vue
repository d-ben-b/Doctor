<!-- @format -->

<template>
  <div class="task-item">
    <div class="task-name">{{ task.name }}</div>
    <div class="task-description">{{ task.description }}</div>
  </div>
</template>

<script>
  export default {
    props: ["task"],
  };
</script>

<style scoped>
  .task-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f5f5f5;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .task-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  .task-name {
    font-size: 22px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }

  .task-description {
    font-size: 16px;
    color: #666;
    line-height: 1.6;
    text-align: center;
  }
</style>
