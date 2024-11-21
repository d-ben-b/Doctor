<!-- @format -->

<template>
  <div class="task-details">
    <!-- 顯示當前任務和分類 -->
    <h1>{{ taskTitle }}</h1>
    <h2>分類: {{ category }}</h2>

    <!-- 填寫新表單 -->
    <div class="form-section">
      <h3>填寫新表單</h3>
      <form @submit.prevent="handleFormSubmission">
        <!-- 基本資訊 -->
        <div class="form-section">
          <h3>基本資訊</h3>
          <label>
            案件編號:
            <input v-model="formData.caseNumber" type="text" required />
          </label>
          <label>
            填報日期:
            <input v-model="formData.reportDate" type="date" required />
          </label>
          <label>
            填報醫師:
            <input v-model="formData.reportDoctor" type="text" required />
          </label>
          <label>
            收案院別:
            <select v-model="formData.hospital" required>
              <option disabled value="">請選擇院別</option>
              <option
                v-for="hospital in hospitalOptions"
                :key="hospital"
                :value="hospital">
                {{ hospital }}
              </option>
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
            縣市:
            <select v-model="formData.city" required>
              <option disabled value="">請選擇縣市</option>
              <option v-for="city in cityOptions" :key="city" :value="city">
                {{ city }}
              </option>
            </select>
          </label>
          <label>
            出生日期:
            <input v-model="formData.birthDate" type="date" required />
          </label>
        </div>

        <!-- 家長資料 -->
        <div class="form-section">
          <h3>家長資料</h3>
          <!-- 父親資料 -->
          <div class="parent-section">
            <h4>父親資料</h4>
            <label>
              父親姓名:
              <input v-model="formData.fatherName" type="text" required />
            </label>
            <label>
              父親身分證號:
              <input v-model="formData.fatherID" type="text" />
            </label>
            <label>
              特殊說明:
              <textarea v-model="formData.fatherDescription"></textarea>
            </label>
          </div>
          <!-- 母親資料 -->
          <div class="parent-section">
            <h4>母親資料</h4>
            <label>
              母親姓名:
              <input v-model="formData.motherName" type="text" required />
            </label>
            <label>
              母親身分證號:
              <input v-model="formData.motherID" type="text" />
            </label>
            <label>
              特殊說明:
              <textarea v-model="formData.motherDescription"></textarea>
            </label>
          </div>
        </div>

        <!-- 健康與個案來源 -->
        <div class="form-section">
          <h3>健康與個案來源</h3>
          <label>
            國籍:
            <select v-model="formData.nationality" required>
              <option value="1">本國籍</option>
              <option value="2">非本國籍</option>
            </select>
          </label>
          <label v-if="formData.nationality === '2'">
            非本國籍說明:
            <textarea v-model="formData.nationalityDescription"></textarea>
          </label>
          <label>
            幼兒醫療史或健康相關說明:
            <textarea v-model="formData.healthDescription"></textarea>
          </label>
          <label>
            個案來源:
            <select v-model="formData.caseSource" required>
              <option value="2">周產期高風險追蹤關懷計畫</option>
              <option value="3">其他中央主管機關指定收案</option>
              <option value="4">地方衛生局指定收案</option>
            </select>
          </label>
          <label
            v-if="formData.caseSource === '3' || formData.caseSource === '4'">
            個案來源說明:
            <textarea v-model="formData.caseSourceDescription"></textarea>
          </label>
        </div>

        <!-- 提交按鈕 -->
        <button type="submit">提交表單</button>
      </form>
    </div>

    <!-- 歷史記錄 -->
    <div class="history-section">
      <h3>歷史記錄</h3>
      <ul class="history-list">
        <li
          class="history-item"
          v-for="(record, index) in historyRecords"
          :key="index">
          <p><strong>任務:</strong> {{ record.task }}</p>
          <p><strong>分類:</strong> {{ record.category }}</p>
          <p><strong>案件編號:</strong> {{ record.caseNumber }}</p>
          <p><strong>填報醫師:</strong> {{ record.reportDoctor }}</p>
          <p><strong>健康狀況:</strong> {{ record.healthDescription }}</p>
          <p><strong>時間:</strong> {{ formatTimestamp(record.timestamp) }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import { ref, onMounted } from "vue";
  import { useRoute } from "vue-router";
  import axios from "axios";

  export default {
    name: "TaskDetails",
    setup() {
      const currentRoute = useRoute();
      const category = ref(currentRoute.query.category || "未知分類");
      const taskTitle = ref(currentRoute.query.task || "未知任務");

      const formData = ref({
        caseNumber: "",
        reportDate: "",
        reportDoctor: "",
        hospital: "",
        startDate: "",
        endDate: "",
        childName: "",
        childID: "",
        noID: false,
        gender: "",
        city: "",
        birthDate: "",
        phone: "",
        address: "",
        fatherName: "",
        fatherID: "",
        fatherDescription: "",
        motherName: "",
        motherID: "",
        motherDescription: "",
        nationality: "",
        nationalityDescription: "",
        healthDescription: "",
        caseSource: "",
        caseSourceDescription: "",
      });

      const historyRecords = ref([]);

      const hospitalOptions = ref(["醫院A", "醫院B", "醫院C", "醫院D"]);
      const cityOptions = ref([
        "臺北市",
        "新北市",
        "桃園市",
        "臺中市",
        "高雄市",
      ]);

      const formatTimestamp = (timestamp) => {
        if (!timestamp) return "未知時間";
        const formattedDate = new Date(timestamp);
        return formattedDate.toLocaleString("zh-TW", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        });
      };

      const fetchHistoryRecords = async () => {
        try {
          const response = await axios.get(
            `http://127.0.0.1:5000/history?task=${taskTitle.value}`,
            {
              headers: {
                Authorization: localStorage.getItem("token"), // 確保 token 正確存儲並傳遞
              },
            }
          );
          historyRecords.value = response.data || [];
        } catch (error) {
          console.error("無法加載歷史記錄", error);
        }
      };

      const handleFormSubmission = async () => {
        try {
          const response = await axios.post("http://127.0.0.1:5000/history", {
            ...formData.value,
            task: taskTitle.value,
            category: category.value,
            timestamp: new Date().toISOString(),
          });
          historyRecords.value.push(response.data);
          alert("表單提交成功！");
        } catch (error) {
          console.error("提交表單失敗", error);
          alert("表單提交失敗，請稍後重試！");
        }
      };

      onMounted(fetchHistoryRecords);

      return {
        category,
        taskTitle,
        formData,
        historyRecords,
        hospitalOptions,
        cityOptions,
        formatTimestamp,
        handleFormSubmission,
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

  .form-section,
  .history-section {
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
