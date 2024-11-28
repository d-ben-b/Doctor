from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json
import uuid
import os

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
            reportName TEXT,
            reportPlace TEXT,
            startDate TEXT,
            endDate TEXT,
            childName TEXT,
            childID TEXT,
            noID BOOLEAN,
            gender TEXT,
            birthDate TEXT,
            parentName TEXT,
            parentID TEXT,
            parentDescription TEXT,
            parentPhone TEXT,
            socialWorkerName TEXT,
            socialWorkerUnit TEXT,
            socialWorkerPhone TEXT,
            timestamp TEXT,
            caseTask TEXT
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
                    str(record.get("reportName", "")),
                    str(record.get("reportPlace", "")),
                    str(record.get("startDate", "")),
                    str(record.get("endDate", "")),
                    str(record.get("childName", "")),
                    str(record.get("childID", "")),
                    int(record.get("noID", 0)),
                    str(record.get("gender", "")),
                    str(record.get("birthDate", "")),
                    str(record.get("parentName", "")),
                    str(record.get("parentID", "")),
                    str(record.get("parentPhone", "")),  # 加入聯絡人電話字段
                    str(record.get("parentDescription", "")),
                    str(record.get("socialWorkerName", "")),
                    str(record.get("socialWorkerUnit", "")),
                    str(record.get("socialWorkerPhone", "")),
                    str(record.get("caseTask", "")),  # 加入收案項目字段
                    str(record.get("timestamp", ""))
                )

                cursor.execute('''
                    INSERT OR IGNORE INTO history (
                        id, caseNumber, reportDate, reportName, reportPlace,
                        startDate, endDate, childName, childID, noID,
                        gender, birthDate, parentName, parentID, parentPhone, parentDescription,
                        socialWorkerName, socialWorkerUnit, socialWorkerPhone, caseTask, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            return jsonify({"message": "Login successful", "token": user[3],"id":user[0]}), 200
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

        if token.startswith("Bearer "):
            token = token[len("Bearer "):]

        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()

        # 驗證 token 是否有效
        cursor.execute('''
            SELECT * FROM login WHERE token = ?
        ''', (token,))
        user = cursor.fetchone()
        if not user:
            connection.close()
            return jsonify({"message": "Invalid token"}), 403

        # 查詢所有歷史資料，支持條件篩選
        query = '''
            SELECT id, caseNumber, reportDate, reportName, reportPlace, 
                   startDate, endDate, childName, childID, noID, gender, 
                   birthDate, parentName, parentID, parentPhone, parentDescription, 
                   socialWorkerName, socialWorkerUnit, socialWorkerPhone, 
                   caseTask, timestamp
            FROM history
        '''
        params = []

        # 可選條件篩選
        start_date = request.args.get("startDate")
        end_date = request.args.get("endDate")
        if start_date:
            query += " WHERE reportDate >= ?"
            params.append(start_date)
        if end_date:
            query += " AND reportDate <= ?" if start_date else " WHERE reportDate <= ?"
            params.append(end_date)

        cursor.execute(query, params)
        records = cursor.fetchall()
        connection.close()

        # 將查詢結果格式化為 JSON
        history_list = [
            {
                "id": record[0],
                "caseNumber": record[1],
                "reportDate": record[2],
                "reportName": record[3],
                "reportPlace": record[4],
                "startDate": record[5],
                "endDate": record[6],
                "childName": record[7],
                "childID": record[8],
                "noID": bool(record[9]),
                "gender": record[10],
                "birthDate": record[11],
                "parentName": record[12],
                "parentID": record[13],
                "parentPhone": record[14],
                "parentDescription": record[15],
                "socialWorkerName": record[16],
                "socialWorkerUnit": record[17],
                "socialWorkerPhone": record[18],
                "caseTask": record[19],
                "timestamp": record[20]
            }
            for record in records
        ]

        # 返回 JSON 格式的資料
        return jsonify(history_list)
    except Exception as e:
        # 返回錯誤訊息
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


@app.route('/history', methods=['POST'])
def add_history_record():
    try:
        # 從請求中獲取 JSON 數據
        data = request.json

        # 簡化的必填欄位列表
        required_fields = [
            "caseNumber", "reportDate", "reportName", "reportPlace",
            "startDate", "endDate", "childName", "gender", "birthDate",
            "parentName", "socialWorkerName", "socialWorkerUnit", "socialWorkerPhone"
        ]

        # 驗證必填欄位是否存在且非空
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"message": f"Missing or empty field: {field}"}), 400

        # 生成唯一 ID，若請求中沒有提供 ID 則自動生成
        record_id = data.get("id", str(uuid.uuid4()))

        # 確保 timestamp 存在，若未提供則自動生成
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()

        # 插入數據到資料表
        cursor.execute('''
            INSERT INTO history (
                id, caseNumber, reportDate, reportName, reportPlace, startDate, endDate,
                childName, childID, noID, gender, birthDate, parentName, parentID,
                parentPhone, parentDescription, socialWorkerName, socialWorkerUnit,
                socialWorkerPhone, caseTask, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record_id, data["caseNumber"], data["reportDate"], data["reportName"],
            data["reportPlace"], data["startDate"], data["endDate"], data["childName"],
            data.get("childID", ""), int(data.get("noID", 0)
                                         ), data["gender"], data["birthDate"],
            data["parentName"], data.get(
                "parentID", ""), data.get("parentPhone", ""),
            data.get("parentDescription",
                     ""), data["socialWorkerName"], data["socialWorkerUnit"],
            data["socialWorkerPhone"], data.get("caseTask", ""), timestamp
        ))

        # 提交更改並關閉連接
        connection.commit()
        connection.close()

        # 返回成功響應
        return jsonify({"message": "Record added successfully", "id": record_id}), 201

    except Exception as e:
        # 捕獲並回應任何異常
        return jsonify({"message": f"Error: {e}"}), 500


@app.route('/history/<string:id>', methods=['PUT'])
def update_history_record(id):
    try:
        # 從請求中獲取 JSON 數據
        data = request.json

        # 驗證必填欄位
        required_fields = [
            "caseNumber", "reportDate", "reportName", "reportPlace",
            "startDate", "endDate", "childName", "gender", "birthDate",
            "parentName", "socialWorkerName", "socialWorkerUnit", "socialWorkerPhone"
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"message": f"Missing or empty field: {field}"}), 400

        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()

        # 更新指定 ID 的數據
        cursor.execute('''
            UPDATE history
            SET caseNumber = ?, reportDate = ?, reportName = ?, reportPlace = ?,
                startDate = ?, endDate = ?, childName = ?, childID = ?, noID = ?,
                gender = ?, birthDate = ?, parentName = ?, parentID = ?, parentPhone = ?,
                parentDescription = ?, socialWorkerName = ?, socialWorkerUnit = ?,
                socialWorkerPhone = ?, caseTask = ?, timestamp = ?
            WHERE id = ?
        ''', (
            data["caseNumber"], data["reportDate"], data["reportName"], data["reportPlace"],
            data["startDate"], data["endDate"], data["childName"], data.get(
                "childID", ""),
            int(data.get("noID", 0)
                ), data["gender"], data["birthDate"], data["parentName"],
            data.get("parentID", ""), data.get("parentPhone",
                                               ""), data.get("parentDescription", ""),
            data["socialWorkerName"], data["socialWorkerUnit"], data["socialWorkerPhone"],
            data.get("caseTask", ""), datetime.now().isoformat(), id
        ))

        # 提交更改並關閉連接
        connection.commit()
        connection.close()

        # 返回成功響應
        return jsonify({"message": "Record updated successfully", "id": id}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


@app.route('/history/<id>', methods=['DELETE'])
def delete_history_record(id):
    try:
        # 連接資料庫
        connection = sqlite3.connect("app.db")
        cursor = connection.cursor()

        # 刪除指定 ID 的數據
        cursor.execute('DELETE FROM history WHERE id = ?', (id,))

        # 提交更改並關閉連接
        connection.commit()
        connection.close()

        # 返回成功響應
        return jsonify({"message": "Record deleted successfully", "id": id}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500



# 主程式啟動
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
