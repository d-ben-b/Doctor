import sqlite3

# 連接資料庫
connection = sqlite3.connect("app.db")
cursor = connection.cursor()

# 查詢資料表結構
cursor.execute("PRAGMA table_info(history)")
columns = cursor.fetchall()

# 打印資料表結構
print("資料表結構：")
for column in columns:
    print(column)

# 關閉連線
connection.close()
