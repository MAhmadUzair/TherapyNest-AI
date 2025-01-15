import axios from "axios";

// Create an instance of Axios
const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000", // Replace with your Django API base URL
  timeout: 100000, // Set a timeout for requests (optional)
  headers: {
    "Content-Type": "application/json", // Set default headers
    Accept: "application/json",
  },
});

// Interceptors (optional)
// Request Interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    // Add authentication tokens or other custom logic here
    const token = localStorage.getItem("authToken"); // Example: Fetch token from localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor
axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle global errors here (e.g., token expiration, API errors)
    console.error("API Error:", error);
    return Promise.reject(error);
  }
);

export default axiosInstance;
