import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';

async function fetchProject(slug) {
  const response = await api.get(`/projects/${slug}/`);
  return response.data || null;
}

export default function ProjectDetailPage() {
  const { slug } = useParams();
  const query = useQuery({ queryKey: ['project', slug], queryFn: () => fetchProject(slug) });
  const project = query.data;

  if (query.isLoading) return <div className="page-shell content-section loading-card">Loading project…</div>;
  if (query.isError || !project) return <div className="page-shell content-section error-card">Project not found.</div>;

  return (
    <article className="page-shell content-section article-layout">
      <Link to="/projects" className="text-link">← Back to projects</Link>
      <img className="article-cover" src={project.cover_image || 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=1400&q=80'} alt={project.title} />
      <h1>{project.title}</h1>
      <div className="meta-row">
        <span>{project.category || 'Web'}</span>
        <span>{project.completed_date || 'Recently completed'}</span>
      </div>
      <p className="lead-copy">{project.summary || project.description}</p>
      <div className="tag-list">
        {(project.tech_stack || []).map((skill) => <span key={skill.id || skill.name} className="chip">{skill.name || skill}</span>)}
      </div>
      <div className="cta-row">
        {project.live_url ? <a href={project.live_url} target="_blank" rel="noreferrer" className="button primary">Live demo</a> : null}
        {project.github_url ? <a href={project.github_url} target="_blank" rel="noreferrer" className="button secondary">GitHub</a> : null}
      </div>
      <div className="rich-content">
        <p>{project.description}</p>
      </div>
    </article>
  );
}
