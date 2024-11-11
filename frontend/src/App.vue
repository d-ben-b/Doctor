<!-- @format -->

<template>
  <div class="navbar">
    <img src="\OIP.jpg" alt="" v-show="login" />
    <h2>專責醫師平台</h2>
    <button class="button remind" v-show="login">提醒</button>
    <button class="button logout" @click="toggleLogin" v-show="login">
      登出
    </button>
    <hr />
  </div>

  <!-- 登入元件 -->
  <login
    :workList="workList"
    @toggle-login="receiveEmit"
    v-show="!login"></login>

  <!-- 個人資訊區塊 -->
  <div class="info" v-show="login">
    <!-- 任務列表 -->
    <task
      v-for="(work, index) in personal_works"
      :key="index"
      :task="work"
      v-show="task"
      @click="showForm(work.name)"></task>

    <!-- 表單列表，根據選定的工作顯示相關表單 -->
    <personal-form
      v-for="(form, index) in filteredForms"
      :key="index"
      :form="form"
      v-show="form && !task && !write"
      @click="toggleWrite"></personal-form>

    <!-- 寫新表單區域 -->
    <write-new v-show="write" @submit="resetStates"></write-new>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        login: false,
        task: true,
        form: false,
        write: false,
        selectedTaskName: "", // 用於儲存當前選中的工作名稱
        workList: [
          {
            work_place: "單位 A",
            work_names: ["局處A", "局處B", "局處C"],
          },
          {
            work_place: "單位 B",
            work_names: ["局處A", "局處B", "局處C"],
          },
          {
            work_place: "單位 C",
            work_names: ["局處A", "局處B", "局處C"],
          },
        ],
        personal_works: [
          { name: "工作 A", description: "描述A" },
          { name: "工作 B", description: "描述B" },
          { name: "工作 C", description: "描述C" },
        ],
        personal_forms: [
          { name: "表單 A", description: "描述A" },
          { name: "表單 A - 1", description: "描述A - 1" },
          { name: "表單 B", description: "描述B" },
          { name: "表單 C", description: "描述C" },
          { name: "表單 B - 1", description: "描述B - 1" },
        ],
      };
    },

    computed: {
      filteredForms() {
        // 過濾出與選定工作名稱相關的表單
        return this.personal_forms.filter((form) =>
          form.name.includes(this.selectedTaskName)
        );
      },
    },

    methods: {
      receiveEmit() {
        this.login = !this.login;
        this.resetStates();
      },
      showForm(taskName) {
        // 根據點擊的工作名稱來顯示對應的表單
        this.selectedTaskName = taskName.split(" ")[1] || "";
        this.task = false;
        this.form = true;
        this.write = false;
      },
      toggleWrite() {
        this.write = !this.write;
        if (this.write) {
          this.form = false;
        }
      },
      toggleLogin() {
        this.login = !this.login;
        this.resetStates();
      },
      resetStates() {
        this.task = true;
        this.form = false;
        this.write = false;
        this.selectedTaskName = "";
      },
    },
  };
</script>

<style scoped>
  /* Navbar 樣式 */
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 25px;
    background-color: #f8f9fa;
    border-bottom: 1px solid #ddd;
  }

  img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
  }

  h2 {
    margin: 0;
    flex-grow: 1;
    text-align: center;
    font-size: 24px;
    color: #333;
  }

  .button {
    padding: 8px 12px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .remind {
    background-color: #ffa500;
    color: #fff;
    border: none;
  }

  .remind:hover {
    background-color: #ff9500;
  }

  .logout {
    background-color: #ff4500;
    color: #fff;
    border: none;
  }

  .logout:hover {
    background-color: #e03e00;
  }

  /* Info 區塊樣式 */
  .info {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  /* Task 項目樣式 */
  .task-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
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
    font-size: 20px;
    font-weight: 600;
    color: #333;
    margin-bottom: 5px;
  }

  .task-description {
    font-size: 16px;
    color: #666;
    text-align: center;
    line-height: 1.5;
  }

  /* Form 項目樣式 */
  .personal-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #fdfdfd;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.3s;
  }

  .personal-form:hover {
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
  }

  .form-name {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }

  .form-description {
    font-size: 16px;
    color: #555;
    line-height: 1.6;
    text-align: center;
  }

  /* Write New 表單樣式 */
  .write-new {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    border: 2px dashed #007bff;
    border-radius: 8px;
    background-color: #e7f1ff;
    color: #007bff;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
  }

  .write-new:hover {
    background-color: #d0e6ff;
    color: #0056b3;
  }
</style>
