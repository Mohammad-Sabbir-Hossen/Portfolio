import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import api from '../api/axios';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('portfolio_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(true);

  const login = ({ access, refresh, user: nextUser }) => {
    localStorage.setItem('portfolio_access_token', access);
    localStorage.setItem('portfolio_refresh_token', refresh);
    localStorage.setItem('portfolio_user', JSON.stringify(nextUser));
    setUser(nextUser);
  };

  const logout = () => {
    localStorage.removeItem('portfolio_access_token');
    localStorage.removeItem('portfolio_refresh_token');
    localStorage.removeItem('portfolio_user');
    setUser(null);
  };

  useEffect(() => {
    const restoreSession = async () => {
      const token = localStorage.getItem('portfolio_access_token');
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await api.get('/auth/me/');
        const nextUser = response.data;
        localStorage.setItem('portfolio_user', JSON.stringify(nextUser));
        setUser(nextUser);
      } catch {
        logout();
      } finally {
        setLoading(false);
      }
    };

    restoreSession();
  }, []);

  const value = useMemo(
    () => ({
      user,
      isOwner: Boolean(user && (user.is_owner || user.is_superuser)),
      login,
      logout,
      loading,
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
