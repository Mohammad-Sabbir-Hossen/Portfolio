import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const response = await api.post('/auth/login/', form);
      login(response.data);
      const fallbackPath = location.state?.from || '/dashboard';
      navigate(fallbackPath, { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page-shell auth-shell">
      <div className="auth-card">
        <span className="eyebrow">Owner access</span>
        <h1>Sign in</h1>
        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Email
            <input type="email" name="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} className="text-input" required />
          </label>
          <label>
            Password
            <input type="password" name="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} className="text-input" required />
          </label>
          {error ? <p className="error-message">{error}</p> : null}
          <button type="submit" className="button primary" disabled={isSubmitting}>
            {isSubmitting ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
      </div>
    </div>
  );
}
