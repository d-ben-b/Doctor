const express = require('express');
const router = express.Router();
const db = require('../db');
const moment = require('moment'); // 引入 moment 套件

// 獲取所有案例
router.get('/history', (req, res) => {
  const sql = 'SELECT * FROM history';

  db.query(sql, (err, results) => {
    if (err) {
      console.error('查詢案例歷史時發生錯誤', err);
      return res.status(500).json({ message: '伺服器錯誤' });
    }

    res.json(results);
  });
});

// 新增案例
router.post('/history', (req, res) => {
  const data = req.body;

  // 處理日期時間欄位
  const dateFields = ['report_date', 'start_date', 'end_date', 'birth_date', 'timestamp'];
  dateFields.forEach(field => {
    if (data[field]) {
      const parsedDate = moment(data[field]).format('YYYY-MM-DD HH:mm:ss');
      if (parsedDate === 'Invalid date') {
        console.error(`無效的日期時間格式：${field}`);
        return res.status(400).json({ message: `無效的日期時間格式：${field}` });
      } else {
        data[field] = parsedDate;
      }
    }
  });

  const sql = 'INSERT INTO history SET ?';

  db.query(sql, data, (err, result) => {
    if (err) {
      console.error('新增案例時發生錯誤：', err);
      return res.status(500).json({ message: '伺服器錯誤' });
    }

    res.json({ message: '新增案例成功', id: result.insertId });
  });
});

// 更新案例
router.put('/history/:id', (req, res) => {
  const id = req.params.id;
  const data = req.body;

  // 處理日期時間欄位
  const dateFields = ['report_date', 'start_date', 'end_date', 'birth_date', 'timestamp'];
  dateFields.forEach(field => {
    if (data[field]) {
      const parsedDate = moment(data[field]).format('YYYY-MM-DD HH:mm:ss');
      if (parsedDate === 'Invalid date') {
        console.error(`無效的日期時間格式：${field}`);
        return res.status(400).json({ message: `無效的日期時間格式：${field}` });
      } else {
        data[field] = parsedDate;
      }
    }
  });

  const sql = 'UPDATE history SET ? WHERE id = ?';

  db.query(sql, [data, id], (err, result) => {
    if (err) {
      console.error('更新案例時發生錯誤', err);
      return res.status(500).json({ message: '伺服器錯誤' });
    }

    res.json({ message: '更新案例成功' });
  });
});

// 刪除案例
router.delete('/history/:id', (req, res) => {
  const id = req.params.id;
  const sql = 'DELETE FROM history WHERE id = ?';

  db.query(sql, [id], (err, result) => {
    if (err) {
      console.error('刪除案例時發生錯誤', err);
      return res.status(500).json({ message: '伺服器錯誤' });
    }

    res.json({ message: '刪除案例成功' });
  });
});

// 獲取特定案例
router.get('/history/:id', (req, res) => {
  const id = req.params.id;
  const sql = 'SELECT * FROM history WHERE id = ?';

  db.query(sql, [id], (err, results) => {
    if (err) {
      console.error('查詢案例時發生錯誤', err);
      return res.status(500).json({ message: '伺服器錯誤' });
    }

    if (results.length === 0) {
      return res.status(404).json({ message: '案例不存在' });
    }

    res.json(results[0]);
  });
});

module.exports = router;
