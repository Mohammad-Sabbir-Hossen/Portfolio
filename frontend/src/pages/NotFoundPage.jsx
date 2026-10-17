import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="page-shell content-section not-found">
      <h1>404</h1>
      <p>The page you were looking for does not exist.</p>
      <Link to="/" className="button primary">Go home</Link>
    </div>
  );
}
