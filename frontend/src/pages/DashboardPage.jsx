import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';

async function fetchDashboardStats() {
  const response = await api.get('/dashboard/stats/');
  return response.data || {};
}

export default function DashboardPage() {
  const query = useQuery({ queryKey: ['dashboard-stats'], queryFn: fetchDashboardStats });

  const stats = query.data || {
    total_posts: 0,
    published_posts: 0,
    draft_posts: 0,
    total_projects: 0,
    total_skills: 0,
    total_comments: 0,
    pending_comments: 0,
    total_likes: 0,
    total_views: 0,
    unread_messages: 0,
  };

  return (
    <div className="dashboard-page">
      <h1>Dashboard overview</h1>
      <div className="stats-grid">
        <div className="stat-card"><strong>{stats.total_posts}</strong><span>Total posts</span></div>
        <div className="stat-card"><strong>{stats.published_posts}</strong><span>Published</span></div>
        <div className="stat-card"><strong>{stats.draft_posts}</strong><span>Drafts</span></div>
        <div className="stat-card"><strong>{stats.total_projects}</strong><span>Projects</span></div>
        <div className="stat-card"><strong>{stats.total_skills}</strong><span>Skills</span></div>
        <div className="stat-card"><strong>{stats.unread_messages}</strong><span>Unread messages</span></div>
      </div>
      {query.isLoading ? <div className="loading-card">Loading dashboard metrics…</div> : null}
      {query.isError ? <div className="error-card">Dashboard data is temporarily unavailable.</div> : null}
    </div>
  );
}
