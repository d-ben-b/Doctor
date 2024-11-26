<!-- @format -->

<template>
  <div class="task-details">
    <h1>填寫新表單</h1>

    <div class="form-section">
      <form @submit.prevent="handleFormSubmission">
        <!-- 基本資訊 -->
        <div class="form-section">
          <h3>基本資訊</h3>
          <label>
            案件編號:
            <input v-model="formData.caseNumber" type="text" required />
          </label>
          <label>
            轉介日期:
            <input v-model="formData.reportDate" type="date" required />
          </label>
          <label>
            填表人姓名:
            <input v-model="formData.reportName" type="text" required />
          </label>
          <label>
            填表人單位：
            <select v-model="formData.reportPlace" required>
              <option value="1">衛生局</option>
              <option value="2">社會局</option>
            </select>
          </label>
          <label>
            開始日期:
            <input v-model="formData.startDate" type="date" required />
          </label>
          <label>
            結束日期:
            <input v-model="formData.endDate" type="date" required />
          </label>
        </div>

        <!-- 個案資訊 -->
        <div class="form-section">
          <h3>個案資訊</h3>
          <label>
            幼兒姓名:
            <input v-model="formData.childName" type="text" required />
          </label>
          <label>
            幼兒身分證:
            <input v-model="formData.childID" type="text" />
          </label>
          <label>
            暫無身分證:
            <input v-model="formData.noID" type="checkbox" />
          </label>
          <label>
            性別:
            <select v-model="formData.gender" required>
              <option value="1">男</option>
              <option value="2">女</option>
            </select>
          </label>
          <label>
            出生日期:
            <input v-model="formData.birthDate" type="date" required />
          </label>
        </div>

        <!-- 家長資料 -->
        <div class="form-section">
          <h3>聯絡人資料</h3>
          <div class="parent-section">
            <label>
              聯絡人姓名:
              <input v-model="formData.parentName" type="text" required />
            </label>
            <label>
              聯絡人電話:
              <input v-model="formData.parentPhone" type="text" required />
            </label>
            <label>
              聯絡人身分證號:
              <input v-model="formData.parentID" type="text" />
            </label>
            <label>
              聯絡人關係:
              <textarea v-model="formData.parentDescription"></textarea>
            </label>
          </div>
        </div>

        <!-- 社工資料 -->
        <div class="form-section">
          <h3>社工資料</h3>
          <label>
            社工姓名:
            <input v-model="formData.socialWorkerName" type="text" required />
          </label>
          <label>
            社工單位:
            <select v-model="formData.socialWorkerUnit" required>
              <option value="1">衛生局</option>
              <option value="2">社會局</option>
            </select>
          </label>
          <label>
            社工電話:
            <input v-model="formData.socialWorkerPhone" type="text" required />
          </label>
        </div>
        <label>
          收案項目:
          <select v-model="formData.caseTask" required>
            <option disabled value="">請選擇收案項目</option>
            <option v-for="task in taskOptions" :key="task" :value="task">
              {{ task }}
            </option>
          </select>
        </label>
        <!-- 提交按鈕 -->
        <button type="submit">提交表單</button>
      </form>
    </div>
  </div>
</template>

<script>
  import { ref } from "vue";
  import { ReadAPI } from "@/composables/useNavigation";

  export default {
    name: "TaskDetails",
    setup() {
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
        parentDescription: "",
        parentPhone: "",
        socialWorkerName: "",
        socialWorkerUnit: "",
        socialWorkerPhone: "",
        caseTask: "",
      });
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

      const handleFormSubmission = async () => {
        try {
          // 假設 ReadAPI 是一個處理 POST 請求的函數
          const response = await ReadAPI("/history", "POST", formData.value);
          if (response.status === 201) {
            alert("表單提交成功！");
          } else {
            console.error("提交錯誤:", response);
            alert("表單提交失敗！");
          }
        } catch (error) {
          console.error("提交失敗:", error);
          alert("表單提交失敗，請稍後再試！");
        }
      };

      return {
        formData,
        handleFormSubmission,
        taskOptions,
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
  }

  button:hover {
    background-color: #0056b3;
  }
</style>
