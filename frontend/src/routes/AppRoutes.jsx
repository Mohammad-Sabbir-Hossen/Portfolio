import { Navigate, Outlet, Route, Routes, Link } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';
import ProtectedRoute from './ProtectedRoute';
import HomePage from '../pages/HomePage';
import AboutPage from '../pages/AboutPage';
import ProjectListPage from '../pages/ProjectListPage';
import ProjectDetailPage from '../pages/ProjectDetailPage';
import BlogListPage from '../pages/BlogListPage';
import BlogDetailPage from '../pages/BlogDetailPage';
import ContactPage from '../pages/ContactPage';
import LoginPage from '../pages/LoginPage';
import DashboardPage from '../pages/DashboardPage';
import NotFoundPage from '../pages/NotFoundPage';

function PublicLayout() {
  return (
    <>
      <Navbar />
      <main>
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

function DashboardLayout() {
  return (
    <div className="dashboard-shell page-shell">
      <aside className="dashboard-sidebar">
        <div className="dashboard-brand">Admin</div>
        <nav className="dashboard-nav">
          <Link to="/dashboard">Overview</Link>
          <Link to="/dashboard/posts">Posts</Link>
          <Link to="/dashboard/projects">Projects</Link>
          <Link to="/dashboard/skills">Skills</Link>
          <Link to="/dashboard/comments">Comments</Link>
          <Link to="/dashboard/messages">Messages</Link>
          <Link to="/dashboard/profile">Profile</Link>
        </nav>
      </aside>
      <div className="dashboard-content">
        <Outlet />
      </div>
    </div>
  );
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/projects" element={<ProjectListPage />} />
        <Route path="/projects/:slug" element={<ProjectDetailPage />} />
        <Route path="/blog" element={<BlogListPage />} />
        <Route path="/blog/:slug" element={<BlogDetailPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Route>

      <Route element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/dashboard/posts" element={<DashboardPage />} />
        <Route path="/dashboard/projects" element={<DashboardPage />} />
        <Route path="/dashboard/skills" element={<DashboardPage />} />
        <Route path="/dashboard/comments" element={<DashboardPage />} />
        <Route path="/dashboard/messages" element={<DashboardPage />} />
        <Route path="/dashboard/profile" element={<DashboardPage />} />
      </Route>

      <Route path="*" element={<NotFoundPage />} />
      <Route path="/404" element={<NotFoundPage />} />
      <Route path="/index.html" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
