import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';

const getArrayData = (responseData) => {
  if (Array.isArray(responseData)) return responseData;
  if (Array.isArray(responseData?.results)) return responseData.results;
  return [];
};

async function fetchProjects() {
  const response = await api.get('/projects/', { params: { page: 1 } });
  return response.data || { results: [] };
}

export default function ProjectListPage() {
  const [page, setPage] = useState(1);
  const query = useQuery({ queryKey: ['projects', page], queryFn: fetchProjects });
  const projects = getArrayData(query.data);

  return (
    <div className="page-shell content-section">
      <div className="section-heading">
        <span className="eyebrow">Projects</span>
        <h1>Selected work.</h1>
      </div>
      {query.isLoading ? <div className="loading-card">Loading projects…</div> : null}
      {query.isError ? <div className="error-card">Unable to load projects. <button type="button" onClick={() => query.refetch()} className="button secondary">Retry</button></div> : null}
      {!query.isLoading && !query.isError && !projects.length ? <div className="empty-box">No projects found.</div> : null}
      {!query.isLoading && !query.isError && projects.length ? (
        <div className="card-grid three-up">
          {projects.map((project) => (
            <Link key={project.slug || project.id} to={`/projects/${project.slug}`} className="project-card card">
              <img src={project.cover_image || 'https://images.unsplash.com/photo-1522542550221-31fd19575a2d?auto=format&fit=crop&w=1200&q=80'} alt={project.title} />
              <div className="card-body">
                <span className="chip">{project.category || 'Web'}</span>
                <h3>{project.title}</h3>
                <p>{project.summary || project.description}</p>
              </div>
            </Link>
          ))}
        </div>
      ) : null}

      <div className="pagination-row">
        <button type="button" className="button ghost" disabled={page <= 1} onClick={() => setPage((current) => Math.max(1, current - 1))}>Previous</button>
        <span>Page {page}</span>
        <button type="button" className="button ghost" onClick={() => setPage((current) => current + 1)}>Next</button>
      </div>
    </div>
  );
}
