process.on('uncaughtException', function (err) {
  console.error('未捕獲的異常：', err);
});

process.on('unhandledRejection', function (reason, p) {
  console.error('未處理的拒絕：', reason);
});

console.log('應用程式開始執行');


const express = require('express');
const app = express();
const authRoutes = require('./routes/auth.js');
const announcementRoutes = require('./routes/announcements.js');
const historyRoutes = require('./routes/history.js');

app.use(express.json());

// route
app.use('/api', authRoutes);
app.use('/api', announcementRoutes);
app.use('/api', historyRoutes);

// on
app.listen(3000, () => {
  console.log('伺服器已啟動在 http://localhost:3000');
});

// debuggggggggg
process.on('uncaughtException', function (err) {
  console.error('未捕獲的異常：', err);
});

process.on('unhandledRejection', function (reason, p) {
  console.error('未處理的拒絕：', reason);
});
