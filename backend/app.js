/** @format */
const cors = require("cors");
const express = require("express");
const app = express();
const authRoutes = require("./routes/auth.js");
const announcementRoutes = require("./routes/announcements.js");
const historyRoutes = require("./routes/history.js");

app.use(cors());

app.use(express.json());

// route
app.use("", authRoutes);
app.use("", announcementRoutes);
app.use("", historyRoutes);

// on
app.listen(3000, () => {
  console.log("伺服器已啟動在 http://localhost:3000");
});

process.on("uncaughtException", function (err) {
  console.error("未捕獲的異常：", err);
});

process.on("unhandledRejection", function (reason, p) {
  console.error("未處理的拒絕：", reason);
});
