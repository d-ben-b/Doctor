<!-- @format -->

<template>
  <div class="case-management">
    <!-- 頁面標題 -->
    <h1>個案管理</h1>
    <button @click="NewCase">+ 填寫新表單</button>

    <!-- 篩選器與搜尋 -->
    <div class="filters">
      <input type="date" v-model="filters.startDate" />
      <select v-model="filters.category">
        <option value="">收案類型</option>
        <option value="衛生局">衛生局</option>
        <option value="社會局">社會局</option>
      </select>
      <input type="text" v-model="filters.keyword" placeholder="搜尋關鍵字" />
      <button @click="fetchCases">搜尋</button>
      <div>每頁顯示的案件數</div>
      <input type="number" v-model="items" />
    </div>

    <!-- 案件列表 -->
    <table class="case-table">
      <thead>
        <tr>
          <th>表單狀況</th>
          <th>轉介日期</th>
          <th>幼兒姓名</th>
          <th>聯絡人姓名</th>
          <th>聯絡人電話</th>
          <th>社工姓名</th>
          <th>社工單位</th>
          <th>社工電話</th>
          <th>收案項目</th>
          <th>填表人單位</th>
          <th>填表人</th>
          <th>更新時間</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="caseItem in paginatedCases" :key="caseItem.id">
          <td>{{ caseItem.caseNumber }}</td>
          <td>{{ caseItem.reportDate }}</td>
          <td>{{ caseItem.childName }}</td>
          <td>{{ caseItem.parentName }}</td>
          <td>{{ caseItem.parentPhone }}</td>
          <td>{{ caseItem.socialWorkerName }}</td>
          <td>{{ caseItem.socialWorkerUnit }}</td>
          <td>{{ caseItem.socialWorkerPhone }}</td>
          <td>{{ caseItem.caseTask }}</td>
          <td>{{ caseItem.reportPlace }}</td>
          <td>{{ caseItem.reportName }}</td>
          <td>{{ formatDate(caseItem.timestamp) }}</td>
          <td>
            <button @click="viewCase(caseItem.id)">查看</button>
            <button @click="editCase(caseItem.id)">編輯</button>
            <button @click="deleteCase(caseItem.id)">刪除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分頁 -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一頁</button>
      <span>頁數 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages || '0'">
        下一頁
      </button>
    </div>
  </div>
</template>

<script>
  import { ref, computed, watch } from "vue";
  import { useNavigation } from "@/composables/useNavigation";
  import { ReadAPI } from "@/composables/useNavigation";

  export default {
    name: "CaseManagement",
    setup() {
      // 案件資料
      const { navigateTo } = useNavigation();
      const allCases = ref([]); // 儲存所有案件
      const paginatedCases = computed(() => {
        // 根據當前頁數和每頁項目數計算顯示的案件
        const start = (currentPage.value - 1) * itemsPerPage.value;
        const end = start + itemsPerPage.value;
        return allCases.value.slice(start, end);
      });
      // 篩選條件
      const filters = ref({
        startDate: "",
        category: "",
        keyword: "",
        reportPlace: "",
      });

      // 分頁
      const currentPage = ref(1);
      const items = ref(10);
      const itemsPerPage = computed(() => items.value); // 每頁顯示的案件數
      const totalPages = computed(() =>
        Math.ceil(allCases.value.length / itemsPerPage.value)
      );

      // 初始化案件資料
      const fetchCases = async () => {
        try {
          var filtered = await ReadAPI("/history", "GET");
          const ID = localStorage.getItem("id");

          if (ID === "2") {
            filtered = filtered.filter((item) => item.reportPlace === "衛生局");
          } else if (auth_token === "3") {
            filtered = filtered.filter((item) => item.reportPlace === "社會局");
          } else {
            filtered = filtered;
          }
          // 篩選條件處理
          if (filters.value.startDate) {
            filtered = filtered.filter(
              (item) =>
                new Date(item.reportDate) >= new Date(filters.value.startDate)
            );
          }
          if (filters.value.category) {
            filtered = filtered.filter(
              (item) => item.socialWorkerUnit === filters.value.category
            );
          }
          if (filters.value.keyword) {
            const keyword = filters.value.keyword;
            filtered = filtered.filter(
              (item) =>
                item.caseNumber.includes(keyword) ||
                item.childName.includes(keyword) ||
                item.caseTask.includes(keyword)
            );
          }

          allCases.value = filtered;
        } catch (error) {
          console.error("無法加載歷史記錄", error);
          alert("無法加載歷史記錄，請稍後再試！");
        }
      };

      // 查看、編輯、刪除功能
      const viewCase = (id) => {
        navigateTo({ path: `/edit`, query: { id, mode: "view" } });
      };
      const editCase = (id) => {
        navigateTo({ path: `/edit`, query: { id, mode: "edit" } });
      };
      const deleteCase = async (id) => {
        const userConfirmed = confirm("確定要刪除此案件嗎？此操作無法恢復！");

        if (!userConfirmed) {
          // 如果用戶取消操作，退出函數
          return;
        }
        try {
          const response = await ReadAPI(`/history/${id}`, "DELETE");
          alert("刪除成功！", response);
        } catch (error) {
          console.error("刪除出錯:", error);
          alert("刪除失敗，請稍後再試！", error);
        }
      };

      // 分頁控制
      const prevPage = () => {
        if (currentPage.value > 1) currentPage.value--;
      };
      const nextPage = () => {
        if (currentPage.value < totalPages.value) currentPage.value++;
      };

      // 格式化日期
      const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleString("zh-TW", { timeZone: "Asia/Taipei" });
      };

      const NewCase = () => {
        navigateTo("/task-details");
      };
      watch(items, () => {
        currentPage.value = 1; // 重設頁碼為 1
        fetchCases();
      });

      // 初始載入
      fetchCases();

      return {
        allCases,
        paginatedCases,
        filters,
        currentPage,
        totalPages,
        formatDate,
        fetchCases,
        viewCase,
        editCase,
        deleteCase,
        prevPage,
        nextPage,
        items,
        NewCase,
      };
    },
  };
</script>

<style scoped>
  .case-management {
    font-family: Arial, sans-serif;
    padding: 20px;
  }

  h1 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
    text-align: center;
  }

  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    border: 1px solid #ddd;
  }

  .filters input,
  .filters select,
  .filters button {
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 5px;
    flex: 1;
    min-width: 150px;
  }

  .filters button {
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }

  .filters button:hover {
    background-color: #0056b3;
  }

  .case-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  .case-table th,
  .case-table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
    font-size: 14px;
  }

  .case-table th {
    background-color: #f1f1f1;
    font-weight: bold;
  }

  .case-table td {
    background-color: #fff;
  }

  .case-table tr:nth-child(even) td {
    background-color: #f9f9f9;
  }

  .case-table button {
    margin: 2px;
    padding: 5px 10px;
    font-size: 12px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .case-table button:nth-child(1) {
    background-color: #28a745;
    color: white;
  }

  .case-table button:nth-child(2) {
    background-color: #ffc107;
    color: white;
  }

  .case-table button:nth-child(3) {
    background-color: #dc3545;
    color: white;
  }

  .case-table button:hover {
    opacity: 0.9;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
  }

  .pagination button {
    padding: 10px 15px;
    font-size: 14px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .pagination button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .pagination span {
    font-size: 14px;
  }
  button {
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    color: white;
    background-color: #28a745;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  button:hover {
    background-color: #218838;
    transform: scale(1.05);
  }
  button:disabled:hover {
    background-color: #ccc; /* 禁用狀態下仍然保持背景顏色 */
    transform: scale(1); /* 禁用時不縮放 */
  }
</style>
