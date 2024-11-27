<!-- @format -->

<template>
  <div class="task-details">
    <h1>{{ mode === "edit" ? "編輯表單" : "查看表單" }}</h1>

    <div class="form-section">
      <h3>{{ mode === "edit" ? "編輯表單" : "查看表單" }}</h3>
      <form @submit.prevent="updateRecord(id, formData)">
        <!-- 基本資訊 -->
        <div class="form-section">
          <h3>基本資訊</h3>
          <label>
            案件編號:
            <input
              v-model="formData.caseNumber"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            轉介日期:
            <input
              v-model="formData.reportDate"
              type="date"
              :disabled="isReadOnly" />
          </label>
          <label>
            填表人姓名:
            <input
              v-model="formData.reportName"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            填表人單位：
            <select v-model="formData.reportPlace" :disabled="isReadOnly">
              <option v-for="unit in Unit" :key="unit" :value="unit">
                {{ unit }}
              </option>
            </select>
          </label>
          <label>
            開始日期:
            <input
              v-model="formData.startDate"
              type="date"
              :disabled="isReadOnly" />
          </label>
          <label>
            結束日期:
            <input
              v-model="formData.endDate"
              type="date"
              :disabled="isReadOnly" />
          </label>
        </div>

        <!-- 個案資訊 -->
        <div class="form-section">
          <h3>個案資訊</h3>
          <label>
            幼兒姓名:
            <input
              v-model="formData.childName"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            幼兒身分證:
            <input
              v-model="formData.childID"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            暫無身分證:
            <input
              v-model="formData.noID"
              type="checkbox"
              :disabled="isReadOnly" />
          </label>
          <label>
            性別:
            <select v-model="formData.gender" :disabled="isReadOnly">
              <option v-for="gender in Genders" :key="gender" :value="gender">
                {{ gender }}
              </option>
            </select>
          </label>
          <label>
            出生日期:
            <input
              v-model="formData.birthDate"
              type="date"
              :disabled="isReadOnly" />
          </label>
        </div>

        <!-- 家長資料 -->
        <div class="form-section">
          <h3>聯絡人資料</h3>
          <label>
            聯絡人姓名:
            <input
              v-model="formData.parentName"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            聯絡人電話:
            <input
              v-model="formData.parentPhone"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            聯絡人身分證號:
            <input
              v-model="formData.parentID"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            聯絡人關係:
            <textarea
              v-model="formData.parentDescription"
              :disabled="isReadOnly"></textarea>
          </label>
        </div>

        <!-- 社工資料 -->
        <div class="form-section">
          <h3>社工資料</h3>
          <label>
            社工姓名:
            <input
              v-model="formData.socialWorkerName"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            社工單位:
            <select v-model="formData.socialWorkerUnit" :disabled="isReadOnly">
              <option v-for="unit in Unit" :key="unit" :value="unit">
                {{ unit }}
              </option>
            </select>
          </label>
          <label>
            社工電話:
            <input
              v-model="formData.socialWorkerPhone"
              type="text"
              :disabled="isReadOnly" />
          </label>
          <label>
            收案項目:
            <select v-model="formData.caseTask" :disabled="isReadOnly">
              <option disabled value="">請選擇收案項目</option>
              <option v-for="task in taskOptions" :key="task" :value="task">
                {{ task }}
              </option>
            </select>
          </label>
        </div>

        <!-- 提交按鈕 -->
        <button v-if="!isReadOnly" type="submit">更新</button>
      </form>
    </div>
    <button @click="return_to_main" v-show="mode == 'view'">返回</button>
  </div>
</template>
<script>
  import { ref, onMounted } from "vue";
  import { useRoute, useRouter } from "vue-router";
  import { ReadAPI, useNavigation } from "@/composables/useNavigation";

  export default {
    name: "TaskDetails",
    setup() {
      const route = useRoute();
      const { navigateTo } = useNavigation();

      const formData = ref({
        caseNumber: "",
        reportDate: "",
        reportName: "",
        reportPlace: "",
        startDate: "",
        endDate: "",
        childName: "",
        childID: "",
        noID: false,
        gender: "",
        birthDate: "",
        parentName: "",
        parentID: "",
        parentPhone: "",
        parentDescription: "",
        socialWorkerName: "",
        socialWorkerUnit: "",
        socialWorkerPhone: "",
        caseTask: "",
      });

      const mode = ref(route.query.mode || "view"); // 'view' or 'edit'
      const id = ref(route.query.id || 0);

      const isReadOnly = ref(mode.value === "view");

      const taskOptions = ref([
        "逾期未接種預防針",
        "B肝高風險",
        "高風險孕產婦",
        "未成年等風險因子孕產婦",
        "新生兒代謝異常個案",
        "低出生體重",
        "早產兒",
        "非法/成癮物質使用者父母",
        "發展遲緩/早期療育需求",
        "領有身心障礙證明者",
        "中低、低收入戶",
        "脆弱家庭",
        "社會局處轉介",
      ]);

      const Unit = ref(["衛生局", "社會局"]);

      const Genders = ref(["男", "女"]);
      const return_to_main = () => {
        navigateTo("/cases");
      };
      // Fetch record details
      const fetchRecord = async () => {
        try {
          const response = await ReadAPI(`/history`, "GET");
          const record = response.find((item) => item.id === id.value);
          formData.value = record;
        } catch (error) {
          console.error("無法加載數據:", error);
        }
      };

      const handleFormSubmission = async () => {
        try {
          await ReadAPI(`/history`, "PUT", formData.value);
          alert("記錄已更新！");
          return_to_main();
        } catch (error) {
          console.error("更新失敗:", error);
          alert("更新失敗，請稍後再試！");
        }
      };
      const updateRecord = async (id, updatedData) => {
        try {
          const response = await ReadAPI(`/history/${id}`, "PUT", updatedData);
          console.log("更新成功:", response);
          alert("記錄已更新！");
          return_to_main();
        } catch (error) {
          console.error("更新出錯:", error);
          alert("更新出錯！");
        }
      };

      onMounted(() => {
        fetchRecord();
      });

      return {
        formData,
        handleFormSubmission,
        taskOptions,
        id,
        mode,
        isReadOnly,
        updateRecord,
        return_to_main,
        Unit,
        Genders,
      };
    },
  };
</script>
<style scoped>
  .task-details {
    padding: 20px;
    font-family: Arial, sans-serif;
  }

  h1,
  h2,
  h3 {
    color: #333;
  }

  .form-section {
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  label {
    display: block;
    margin-bottom: 10px;
    font-weight: bold;
  }

  input,
  textarea,
  select {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
  }

  button {
    display: block;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    margin-top: 20px;
  }

  button:hover {
    background-color: #0056b3;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
</style>
