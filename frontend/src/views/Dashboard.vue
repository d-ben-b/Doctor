<!-- @format -->

<template>
  <div class="dashboard">
    <!-- 主內容區 -->
    <div class="categories">
      <div
        class="category"
        v-for="(category, index) in categories"
        :key="index">
        <h2 class="category-title">{{ category.name }}</h2>
        <ul class="tasks">
          <li
            class="task"
            v-for="(task, idx) in category.tasks"
            :key="idx"
            @click="handleTaskClick(category.name, task)">
            {{ task }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import useNavigation from "@/composables/useNavigation";

  export default {
    setup() {
      const { navigateTo } = useNavigation();

      const handleTaskClick = (category, task) => {
        console.log(`跳轉到 ${category} 的 ${task}`);
        navigateTo(`/task-details?category=${category}&task=${task}`);
      };

      return {
        handleTaskClick,
      };
    },
    data() {
      return {
        categories: [], // 初始化為空數據
      };
    },
    methods: {
      async fetchCategories() {
        // 模擬從 API 加載數據
        try {
          const response = await axios.get("http://localhost:3000/categories");
          this.categories = response.data;
        } catch (error) {
          console.error("加載分類數據失敗", error);
        }
      },
    },
    async mounted() {
      await this.fetchCategories();
    },
  };
</script>

<style scoped>
  /* 整體樣式 */
  .dashboard {
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    padding: 20px;
  }

  /* 頂部標題樣式 */
  .navbar {
    text-align: center;
    padding: 20px 0;
    background-color: #007bff;
    color: white;
    border-radius: 8px;
  }

  .navbar h1 {
    font-size: 24px;
    margin: 0;
  }

  /* 分類區域 */
  .categories {
    display: flex;
    gap: 20px;
    margin-top: 20px;
    flex-wrap: wrap;
    justify-content: center;
  }

  /* 單個分類樣式 */
  .category {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
  }

  .category-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
    color: #333;
    text-align: center;
  }

  /* 任務列表 */
  .tasks {
    list-style-type: none;
    padding: 0;
  }

  .task {
    background-color: #e7f1ff;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
    cursor: pointer;
    text-align: center;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s, transform 0.2s;
  }

  .task:hover {
    background-color: #d0e6ff;
    transform: scale(1.05);
  }

  .task:active {
    background-color: #c0d8ff;
  }
</style>
