import { Link } from 'react-router-dom';
import { FaGithub, FaEnvelope } from 'react-icons/fa';

const currentYear = new Date().getFullYear();

export default function Footer() {
  const year = currentYear;

  return (
    <footer className="site-footer">
      <div className="page-shell footer-inner">
        <div>
          <h3>Mujahid Islam</h3>
          <p>Full-stack developer building practical systems, APIs, and AI-powered product experiences.</p>
        </div>
        <div>
          <h4>Quick links</h4>
          <div className="footer-links">
            <Link to="/about">About</Link>
            <Link to="/projects">Projects</Link>
            <Link to="/blog">Blog</Link>
            <Link to="/contact">Contact</Link>
          </div>
        </div>
        <div>
          <h4>Connect</h4>
          <div className="social-row">
            <a href="https://github.com/mujahid9644" target="_blank" rel="noreferrer" aria-label="GitHub">
              <FaGithub />
            </a>
            <a href="mailto:mujahidislam2540@gmail.com" aria-label="Email">
              <FaEnvelope />
            </a>
          </div>
        </div>
      </div>
      <div className="footer-bottom">© {year} Mujahid Islam. All rights reserved.</div>
    </footer>
  );
}
