/** @format */

const express = require("express");
const router = express.Router();
const db = require("../db");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

//------------------
const saltRounds = 10;
const plainPassword = "123";

bcrypt.hash(plainPassword, saltRounds, function (err, hash) {
  if (err) {
    console.error("加密密碼時發生錯誤：", err);
    return;
  }
  // 將 hash 存入資料庫
  console.log("加密後的密碼：", hash);

  const sql = "UPDATE users SET password = ? WHERE username = ?";
  db.query(sql, [hash, "A"], (err, result) => {
    if (err) {
      console.error("更新密碼時發生錯誤：", err);
      return;
    }
    console.log("密碼已更新");
  });
});
//--------------------

router.post("/login", (req, res) => {
  const { username, password } = req.body;
  const sql = "SELECT * FROM users WHERE username = ?";

  db.query(sql, [username], (err, results) => {
    if (err) {
      console.error("查詢用戶時發生錯誤：", err);
      return res.status(500).json({ message: "伺服器錯誤" });
    }
    if (results.length === 0) {
      return res.status(400).json({ message: "用戶不存在" });
    }

    const user = results[0];

    bcrypt.compare(password, user.password, (err, isMatch) => {
      if (err) {
        console.error("驗證密碼時發生錯誤", err);
        return res.status(500).json({ message: "伺服器錯誤" });
      }
      if (isMatch) {
        const token = jwt.sign({ id: user.id }, "您的密鑰", {
          expiresIn: "1h",
        });
        return res.json({
          token,
          user: { id: user.id, username: user.username },
        });
      } else {
        return res.status(400).json({ message: "密碼錯誤" });
      }
    });
  });
});

module.exports = router;
