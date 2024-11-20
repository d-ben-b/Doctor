const express = require('express');
const router = express.Router();
const db = require('../db');

// All announcements
router.get('/announcements', (req, res) => {
  const sql = `
    SELECT a.id as announcement_id, a.work_place, w.id as work_name_id, w.work_name
    FROM announcements a
    LEFT JOIN work_names w ON a.id = w.announcement_id
  `;

  db.query(sql, (err, results) => {
    if (err) {
      console.error('查詢公告時發生錯誤', err);
      return res.status(500).json({ message: '伺服器錯誤' });
    }

    // make it into Structures
    const announcements = [];
    const announcementMap = {};

    results.forEach(row => {
      const { announcement_id, work_place, work_name } = row;

      if (!announcementMap[announcement_id]) {
        announcementMap[announcement_id] = {
          id: announcement_id,
          work_place: work_place,
          work_names: []
        };
        announcements.push(announcementMap[announcement_id]);
      }

      if (work_name) {
        announcementMap[announcement_id].work_names.push(work_name);
      }
    });

    res.json(announcements);
  });
});

module.exports = router;
