import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';
import { FaHeart, FaShare, FaComment } from 'react-icons/fa';
import api from '../api/axios';

async function fetchPost(slug) {
  const response = await api.get(`/posts/${slug}/`);
  return response.data || null;
}

export default function BlogDetailPage() {
  const { slug } = useParams();
  const query = useQuery({ queryKey: ['post', slug], queryFn: () => fetchPost(slug) });
  const post = query.data;

  if (query.isLoading) return <div className="page-shell content-section loading-card">Loading article…</div>;
  if (query.isError || !post) return <div className="page-shell content-section error-card">Article not found.</div>;

  return (
    <article className="page-shell content-section article-layout">
      <Link to="/blog" className="text-link">← Back to blog</Link>
      <img className="article-cover" src={post.cover_image || 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1400&q=80'} alt={post.title} />
      <h1>{post.title}</h1>
      <div className="meta-row">
        <span>{post.published_at || 'Published recently'}</span>
        <span>{post.reading_time || 5} min read</span>
        <span>{post.views_count || 0} views</span>
      </div>
      <div className="tag-list">
        {(post.tags || []).map((tag) => <span key={tag.slug || tag.id} className="chip">{tag.name}</span>)}
      </div>
      <div className="share-row">
        <button type="button" className="button ghost"><FaHeart /> Like</button>
        <button type="button" className="button ghost"><FaShare /> Share</button>
        <button type="button" className="button ghost"><FaComment /> Comment</button>
      </div>
      <div className="rich-content"><ReactMarkdown>{post.content || post.excerpt}</ReactMarkdown></div>
      <div className="related-posts">
        <h2>Related posts</h2>
        <div className="card-grid three-up">
          <div className="empty-box">Related posts will appear when the API delivers them.</div>
        </div>
      </div>
    </article>
  );
}
