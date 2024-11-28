/** @format */
import axios from "axios";
import { useRouter } from "vue-router";

//const API_BASE_URL = "https://doctor-1-kpce.onrender.com";
const API_BASE_URL = "http://127.0.0.1:5000";

export function useNavigation() {
  const router = useRouter();

  const navigateTo = (path) => {
    router.push(path);
  };

  return {
    navigateTo,
  };
}

export async function ReadAPI(apiType, method = "GET", params = {}) {
  const apiUrl = API_BASE_URL + apiType; // 取得 API URL

  // 設定 request 的 config
  const config = {
    method: method, // 默認是 GET，若需要其他方法可以傳入
    url: apiUrl, // 請求的 URL
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`, // 加入 token
      "Content-Type": "application/json", // 設置內容類型為 JSON
    },
  };

  // 根據請求方法選擇傳遞參數
  if (method === "POST" || method === "PUT" || method === "DELETE") {
    config.data = params; // POST/PUT/DELETE 請求會把 params 作為資料發送
  } else if (method === "GET" && Object.keys(params).length > 0) {
    // 如果是 GET 請求且有參數，則附加在 URL 上
    config.params = params;
  }

  try {
    const response = await axios(config); // 發送請求
    return response.data; // 返回回應資料
  } catch (error) {
    // 錯誤處理：提供更詳細的錯誤訊息
    console.error(
      `Error fetching data from ${apiType} API:`,
      error.response?.data || error.message
    );
    if (error.response) {
      // 如果有回應，根據狀態碼處理
      if (error.response.status === 401) {
        alert("認證失敗，請重新登入！");
      } else if (error.response.status === 404) {
        alert("未找到相關資源！");
      } else {
        alert(`API 錯誤：${error.response.status}`);
      }
    } else {
      alert("網路連線錯誤，請稍後再試！");
    }
    throw error; // 讓錯誤往上層拋出
  }
}
