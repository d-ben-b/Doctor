<!-- @format -->

<template>
  <div class="case-management">
    <!-- 頁面標題 -->
    <h1>個案管理</h1>
    <button @click="NewCase">+ 填寫新表單</button>

    <!-- 篩選器與搜尋 -->
    <div class="filters">
      <input type="date" v-model="filters.startDate" />
      <input type="date" v-model="filters.endDate" />
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
          <!-- TODO：改 -->
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
      <button @click="nextPage" :disabled="currentPage === totalPages">
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
        console.log(itemsPerPage.value);
        return allCases.value.slice(start, end);
      });
      // 篩選條件
      const filters = ref({
        startDate: "",
        endDate: "",
        category: "",
        keyword: "",
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
          console.log(allCases);

          // 篩選條件處理
          if (filters.value.startDate) {
            filtered = filtered.filter(
              (item) =>
                new Date(item.reportDate) >= new Date(filters.value.startDate)
            );
          }
          if (filters.value.endDate) {
            filtered = filtered.filter(
              (item) =>
                new Date(item.reportDate) <= new Date(filters.value.endDate)
            );
          }
          if (filters.value.category) {
            filtered = filtered.filter(
              (item) => item.category === filters.value.category
            );
          }
          if (filters.value.keyword) {
            const keyword = filters.value.keyword.toLowerCase();
            filtered = filtered.filter(
              (item) =>
                item.caseNumber.toLowerCase().includes(keyword) ||
                item.childName.toLowerCase().includes(keyword) ||
                item.task.toLowerCase().includes(keyword)
            );
          }
          allCases.value = filtered;
        } catch (error) {
          console.error("無法加載歷史記錄", error);
          alert("無法加載歷史記錄，請稍後再試！");
        }
        console.log("篩選前的所有資料:", allCases.value);
        console.log("篩選後的資料:", filtered);
      };

      // 查看、編輯、刪除功能
      const viewCase = (id) => alert(`查看案件 ID: ${id}`);
      const editCase = (id) => alert(`編輯案件 ID: ${id}`);
      const deleteCase = (id) => {
        allCases.value = allCases.value.filter((item) => item.id !== id);
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
  .filters {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }

  .case-table {
    width: 100%;
    border-collapse: collapse;
  }

  .case-table th,
  .case-table td {
    border: 1px solid #ddd;
    padding: 8px;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    gap: 10px;
  }
</style>
