import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';

const getArrayData = (responseData) => {
  if (Array.isArray(responseData)) return responseData;
  if (Array.isArray(responseData?.results)) return responseData.results;
  return [];
};

async function fetchPosts({ page, search, category }) {
  const response = await api.get('/posts/', {
    params: {
      page,
      search,
      category,
      ordering: '-published_at',
    },
  });
  return response.data || { results: [] };
}

export default function BlogListPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');

  const query = useQuery({
    queryKey: ['posts', page, search, category],
    queryFn: () => fetchPosts({ page, search, category }),
  });

  const posts = useMemo(() => getArrayData(query.data), [query.data]);

  return (
    <div className="page-shell content-section">
      <div className="section-heading">
        <span className="eyebrow">Blog</span>
        <h1>Notes from the field.</h1>
      </div>
      <div className="toolbar">
        <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search posts" className="text-input" />
        <select value={category} onChange={(event) => setCategory(event.target.value)} className="select-input">
          <option value="">All categories</option>
          <option value="web">Web</option>
          <option value="development">Development</option>
        </select>
      </div>

      {query.isLoading ? <div className="loading-card">Loading posts…</div> : null}
      {query.isError ? <div className="error-card">Unable to load posts. <button type="button" onClick={() => query.refetch()} className="button secondary">Retry</button></div> : null}
      {!query.isLoading && !query.isError && !posts.length ? <div className="empty-box">No posts found for '{search}'.</div> : null}

      {!query.isLoading && !query.isError && posts.length ? (
        <div className="card-grid three-up">
          {posts.map((post) => (
            <Link key={post.slug || post.id} to={`/blog/${post.slug}`} className="post-card card">
              <img src={post.cover_image || 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80'} alt={post.title} />
              <div className="card-body">
                <span className="chip">{post.category?.name || 'Blog'}</span>
                <h3>{post.title}</h3>
                <p>{post.excerpt}</p>
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
