// frontend/src/api.js
import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export async function searchWebsite(url, query) {
  const res = await axios.post(`${API_URL}/search`, { url, query });
  return res.data;
}
