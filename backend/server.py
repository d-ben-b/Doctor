from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

# 創建 Flask 應用程式
app = Flask(__name__)

CORS(app)

def init_db():
    # 連接 SQLite 資料庫
    connection = sqlite3.connect("app.db")
    cursor = connection.cursor()

    # 創建 login 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            token TEXT
        )
    ''')

    # 創建 history 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id TEXT PRIMARY KEY,
            caseNumber TEXT,
            reportDate TEXT,
            reportDoctor TEXT,
            hospital TEXT,
            startDate TEXT,
            endDate TEXT,
            childName TEXT,
            childID TEXT,
            noID BOOLEAN,
            gender TEXT,
            city TEXT,
            birthDate TEXT,
            phone TEXT,
            address TEXT,
            fatherName TEXT,
            fatherID TEXT,
            fatherDescription TEXT,
            motherName TEXT,
            motherID TEXT,
            motherDescription TEXT,
            nationality TEXT,
            nationalityDescription TEXT,
            healthDescription TEXT,
            caseSource TEXT,
            caseSourceDescription TEXT,
            task TEXT,
            category TEXT,
            timestamp TEXT
        )
    ''')

    # 創建 categories 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT,
            tasks TEXT
        )
    ''')

    # 創建 announcementList 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcementList (
            id TEXT PRIMARY KEY,
            work_place TEXT,
            work_names TEXT
        )
    ''')

    # 從 JSON 文件導入資料
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

            # 插入 login 資料
            for user in data["login"]:
                cursor.execute('''
                    INSERT OR IGNORE INTO login (id, username, password, token)
                    VALUES (?, ?, ?, ?)
                ''', (user["id"], user["username"], user["password"], user["token"]))

            # 插入 history 資料
            for record in data["history"]:
                values = (
                    str(record.get("id", "")),
                    str(record.get("caseNumber", "")),
                    str(record.get("reportDate", "")),
                    str(record.get("reportDoctor", "")),
                    str(record.get("hospital", "")),
                    str(record.get("startDate", "")),
                    str(record.get("endDate", "")),
                    str(record.get("childName", "")),
                    str(record.get("childID", "")),
                    int(record.get("noID", 0)),
                    str(record.get("gender", "")),
                    str(record.get("city", "")),
                    str(record.get("birthDate", "")),
                    str(record.get("phone", "")),
                    str(record.get("address", "")),
                    str(record.get("fatherName", "")),
                    str(record.get("fatherID", "")),
                    str(record.get("fatherDescription", "")),
                    str(record.get("motherName", "")),
                    str(record.get("motherID", "")),
                    str(record.get("motherDescription", "")),
                    str(record.get("nationality", "")),
                    str(record.get("nationalityDescription", "")),
                    str(record.get("healthDescription", "")),
                    str(record.get("caseSource", "")),
                    str(record.get("caseSourceDescription", "")),
                    str(record.get("task", "")),
                    str(record.get("category", "")),
                    str(record.get("timestamp", ""))
                )

                cursor.execute('''
                    INSERT OR IGNORE INTO history (
                        id, caseNumber, reportDate, reportDoctor, hospital,
                        startDate, endDate, childName, childID, noID,
                        gender, city, birthDate, phone, address,
                        fatherName, fatherID, fatherDescription, motherName,
                        motherID, motherDescription, nationality, nationalityDescription,
                        healthDescription, caseSource, caseSourceDescription, task, category, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', values)

            # 插入 categories 資料
            for category in data["categories"]:
                cursor.execute('''
                    INSERT OR IGNORE INTO categories (id, name, tasks)
                    VALUES (?, ?, ?)
                ''', (category["id"], category["name"], json.dumps(category["tasks"])))

            # 插入 announcementList 資料
            for announcement in data["announcementList"]:
                cursor.execute('''
                    INSERT OR IGNORE INTO announcementList (id, work_place, work_names)
                    VALUES (?, ?, ?)
                ''', (announcement["id"], announcement["work_place"], json.dumps(announcement["work_names"])))

        # 提交更改
        connection.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        # 關閉資料庫連接
        connection.close()



# 初始化資料庫
init_db()

# 登入 API


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # 驗證輸入是否完整
        if not username or not password:
            return jsonify({"message": "Missing username or password"}), 400

        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM login WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        connection.close()

        # 登入成功返回 token
        if user:
            return jsonify({"message": "Login successful", "token": user[3]})
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

# 查詢歷史紀錄 API


@app.route('/history', methods=['GET'])
def history():
    try:
        token = request.headers.get("Authorization")

        # 驗證 token 是否提供
        if not token:
            return jsonify({"message": "Missing token"}), 401

        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM login WHERE token = ?
        ''', (token,))
        user = cursor.fetchone()

        # 驗證 token 是否有效
        if not user:
            connection.close()
            return jsonify({"message": "Invalid token"}), 403

        # 查詢所有歷史資料
        cursor.execute('''
            SELECT * FROM history
        ''')
        records = cursor.fetchall()
        connection.close()

        # 將查詢結果格式化為 JSON
        history_list = [
            {
                "id": record[0],
                "caseNumber": record[1],
                "reportDate": record[2],
                "reportDoctor": record[3],
                "hospital": record[4],
                "startDate": record[5],
                "endDate": record[6],
                "childName": record[7],
                "childID": record[8],
                "noID": bool(record[9]),
                "gender": record[10],
                "city": record[11],
                "birthDate": record[12],
                "phone": record[13],
                "address": record[14],
                "fatherName": record[15],
                "fatherID": record[16],
                "fatherDescription": record[17],
                "motherName": record[18],
                "motherID": record[19],
                "motherDescription": record[20],
                "nationality": record[21],
                "nationalityDescription": record[22],
                "healthDescription": record[23],
                "caseSource": record[24],
                "caseSourceDescription": record[25],
                "task": record[26],
                "category": record[27],
                "timestamp": record[28]
            }
            for record in records
        ]

        # 返回 JSON 格式的資料
        return jsonify(history_list)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

# 查詢 categories API


@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()

        # 查詢所有 categories
        cursor.execute('''
            SELECT * FROM categories
        ''')
        categories = cursor.fetchall()
        connection.close()

        # 格式化為 JSON
        categories_list = [
            {
                "id": category[0],
                "name": category[1],
                "tasks": json.loads(category[2])
            }
            for category in categories
        ]

        return jsonify(categories_list)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


@app.route('/announcementList', methods=['GET'])
def get_announcement_list():
    try:
        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()

        # 查詢所有 announcementList
        cursor.execute('''
            SELECT * FROM announcementList
        ''')
        announcements = cursor.fetchall()
        connection.close()

        # 格式化為 JSON
        announcement_list = [
            {
                "id": announcement[0],
                "work_place": announcement[1],
                "work_names": json.loads(announcement[2])
            }
            for announcement in announcements
        ]

        return jsonify(announcement_list)
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


# 主程式啟動
if __name__ == '__main__':
    app.run(debug=True)
