# 安裝套件
npm install
npm install express mysql bcrypt jsonwebtoken

# 執行程式
node app.js

# Test (with Postman)
方法：POST
URL：http://localhost:3000/api/login
Headers:
    Content-Type: application/json
Body：
    選擇 raw 和 JSON 格式
    輸入以下內容：
    {
        "username": "A",
        "password": "123"
    }
