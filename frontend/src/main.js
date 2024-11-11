/** @format */

import { createApp } from "vue";
import App from "./App.vue";
import Login from "./components/Login.vue";
import Task from "./components/Task.vue";
import Form from "./components/Form.vue";
import WriteNew from "./components/WriteNew.vue";

const app = createApp(App);
app.component("login", Login);
app.component("task", Task);
app.component("personal-form", Form);
app.component("write-new", WriteNew);
app.mount("#app");
