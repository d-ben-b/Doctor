-- 建立資料庫
CREATE DATABASE my_database;
USE my_database;

-- 用戶表
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  token VARCHAR(255)
);

-- 公告表
CREATE TABLE announcements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  work_place VARCHAR(255) NOT NULL
);

-- 工作名稱表
CREATE TABLE work_names (
  id INT AUTO_INCREMENT PRIMARY KEY,
  announcement_id INT NOT NULL,
  work_name VARCHAR(255) NOT NULL,
  FOREIGN KEY (announcement_id) REFERENCES announcements(id) ON DELETE CASCADE
);

-- 類別表
CREATE TABLE categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- 任務表
CREATE TABLE tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  category_id INT NOT NULL,
  task_name VARCHAR(255) NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 案例歷史表
CREATE TABLE history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  case_number VARCHAR(50) NOT NULL,
  report_date DATE NOT NULL,
  report_doctor VARCHAR(255) NOT NULL,
  hospital VARCHAR(255) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  child_name VARCHAR(255) NOT NULL,
  child_id VARCHAR(20),
  no_id BOOLEAN DEFAULT FALSE,
  gender VARCHAR(10) NOT NULL,
  city VARCHAR(255) NOT NULL,
  birth_date DATE NOT NULL,
  phone VARCHAR(20),
  address VARCHAR(255),
  father_name VARCHAR(255),
  father_id VARCHAR(20),
  father_description TEXT,
  mother_name VARCHAR(255),
  mother_id VARCHAR(20),
  mother_description TEXT,
  nationality VARCHAR(50),
  nationality_description TEXT,
  health_description TEXT,
  case_source INT,
  case_source_description VARCHAR(255),
  task VARCHAR(255),
  category VARCHAR(255),
  timestamp DATETIME NOT NULL
);

-- 插入用戶資料
INSERT INTO users (username, password, token) VALUES
('A', '123', 'abc123'),
('B', '123', 'def456'),
('C', '123', 'ghi789');

-- 插入公告
INSERT INTO announcements (work_place) VALUES
('衛生局'),
('社會局');

-- 插入工作名稱
INSERT INTO work_names (announcement_id, work_name) VALUES
(1, '逾期未接種預防針'),
(1, 'B肝高風險'),
(1, '高風險孕產婦'),
(1, '未成年等風險因子孕產婦'),
(1, '新生兒代謝異常個案'),
(1, '低出生體重'),
(1, '早產兒'),
(1, '非法/成癮物質使用者父母'),
(2, '發展遲緩/早期療育需求'),
(2, '領有身心障礙證明者'),
(2, '中低、低收入戶'),
(2, '脆弱家庭'),
(2, '社會局處轉介');

-- 插入類別
INSERT INTO categories (name) VALUES
('衛生局'),
('社會局');

-- 插入任務
INSERT INTO tasks (category_id, task_name) VALUES
(1, '逾期未接種預防針'),
(1, 'B肝高風險'),
(1, '高風險孕產婦'),
(1, '未成年等風險因子孕產婦'),
(1, '新生兒代謝異常個案'),
(1, '低出生體重'),
(1, '早產兒'),
(1, '非法/成癮物質使用者父母'),
(2, '發展遲緩/早期療育需求'),
(2, '領有身心障礙證明者'),
(2, '中低、低收入戶'),
(2, '脆弱家庭'),
(2, '社會局處轉介');

-- 插入案例歷史資料
INSERT INTO history (
  case_number, report_date, report_doctor, hospital, start_date, end_date,
  child_name, child_id, no_id, gender, city, birth_date, phone, address,
  father_name, father_id, father_description, mother_name, mother_id, mother_description,
  nationality, nationality_description, health_description, case_source, case_source_description,
  task, category, timestamp
) VALUES
('001', '2024-11-16', '陳大明', '臺北市立聯合醫院', '2024-11-01', '2024-12-01',
 '王小明', 'A123456789', FALSE, '男', '臺北市', '2024-01-01', '0912345678', '臺北市中山區南京東路100號',
 '王大明', 'B987654321', '', '李小美', 'C135792468', '',
 '本國籍', '', '過敏體質，需定期追蹤', 3, '地方衛生局指定',
 '逾期未接種預防針', '衛生局', '2024-11-16 07:00:00'),
-- 其他案例資料，請依次插入
('002', '2024-11-15', '林志偉', '新北市立聯合醫院', '2024-11-05', '2024-12-05',
 '林美麗', 'D246810121', FALSE, '女', '新北市', '2024-02-15', '0923456789', '新北市板橋區民生路200號',
 '林大壯', 'E975318642', '因工作需長期出差', '陳美華', 'F864213579', '',
 '本國籍', '', '早產兒，需特別注意', 4, '中央主管機關指定',
 '早產兒', '衛生局', '2024-11-16 08:00:00'),
-- 繼續插入其他案例...

('005', '2024-11-12', '黃國泰', '桃園市立醫院', '2024-11-02', '2024-12-02',
 '黃小傑', 'M102938475', FALSE, '男', '桃園市', '2024-05-15', '0956789012', '桃園市中壢區大同路500號',
 '黃明亮', 'N109283746', '', '簡秋萍', 'O938475102', '',
 '非本國籍', '父親為外籍人士', '需進一步檢查視力', 4, '中央主管機關指定',
 '領有身心障礙證明者', '社會局', '2024-11-16 11:00:00');
sys_config