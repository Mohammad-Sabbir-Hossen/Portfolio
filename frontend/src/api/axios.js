import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

const getVisitorId = () => {
  let visitorId = localStorage.getItem('portfolio_visitor_id');
  if (!visitorId) {
    visitorId = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : `visitor-${Date.now()}`;
    localStorage.setItem('portfolio_visitor_id', visitorId);
  }
  return visitorId;
};

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('portfolio_access_token');
  const visitorId = getVisitorId();

  config.headers = config.headers || {};
  config.headers['X-Visitor-Id'] = visitorId;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      const refreshToken = localStorage.getItem('portfolio_refresh_token');

      if (!refreshToken) {
        localStorage.removeItem('portfolio_access_token');
        localStorage.removeItem('portfolio_refresh_token');
        localStorage.removeItem('portfolio_user');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        originalRequest._retry = true;
        const response = await axios.post(`${API_BASE}/auth/refresh/`, { refresh: refreshToken });
        const nextAccessToken = response.data.access;
        localStorage.setItem('portfolio_access_token', nextAccessToken);
        originalRequest.headers.Authorization = `Bearer ${nextAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('portfolio_access_token');
        localStorage.removeItem('portfolio_refresh_token');
        localStorage.removeItem('portfolio_user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
