import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { FaArrowRight, FaGithub, FaLinkedin, FaDownload, FaEnvelope, FaCodeBranch, FaRocket } from 'react-icons/fa';
import api from '../api/axios';
import {
  portfolioProfile,
  skillGroups as fallbackSkillGroups,
  featuredProjects as fallbackProjects,
  journeySteps,
  certifications,
} from '../data/portfolioData';

const getArrayData = (responseData) => {
  if (Array.isArray(responseData)) return responseData;
  if (Array.isArray(responseData?.results)) return responseData.results;
  return [];
};

async function fetchProfile() {
  const response = await api.get('/profile/');
  return response.data || null;
}

async function fetchSkills() {
  const response = await api.get('/skills/');
  return getArrayData(response.data);
}

async function fetchFeaturedProjects() {
  const response = await api.get('/projects/', { params: { is_featured: true, page: 1 } });
  return getArrayData(response.data).slice(0, 3);
}

function getSkillGroups(items) {
  if (!items.length) return fallbackSkillGroups;

  const map = new Map();
  items.forEach((item) => {
    const category = (item.category || 'other').toLowerCase();
    const label =
      category === 'frontend'
        ? 'Frontend Development'
        : category === 'backend'
          ? 'Backend Development'
          : category === 'database'
            ? 'Databases'
            : category === 'tools'
              ? 'Developer Tools'
              : 'Professional Focus';

    const current = map.get(label) || [];
    current.push(item.name);
    map.set(label, current);
  });

  return [...map.entries()].map(([label, itemsList]) => ({ label, items: itemsList }));
}

export default function HomePage() {
  const profileQuery = useQuery({ queryKey: ['profile'], queryFn: fetchProfile });
  const skillsQuery = useQuery({ queryKey: ['skills', 'featured'], queryFn: fetchSkills });
  const projectsQuery = useQuery({ queryKey: ['projects', 'featured'], queryFn: fetchFeaturedProjects });

  const profileData = profileQuery.data || {};
  const profile = {
    ...portfolioProfile,
    ...profileData,
    name: profileData.name || profileData.full_name || portfolioProfile.name,
    tagline: profileData.tagline || portfolioProfile.title,
    bio: profileData.bio || portfolioProfile.bio,
    email: profileData.email || portfolioProfile.email,
    github: profileData.github || profileData.github_url || portfolioProfile.github,
    linkedin: profileData.linkedin || profileData.linkedin_url || portfolioProfile.linkedin,
    website: profileData.website || portfolioProfile.website,
    resume: profileData.resume_url || profileData.resume || '',
  };

  const skills = getSkillGroups(skillsQuery.data || []);
  const projects = projectsQuery.data?.length ? projectsQuery.data : fallbackProjects;

  return (
    <>
      <section className="hero-section page-shell">
        <div className="hero-copy">
          <span className="hero-badge">{profile.availability || 'Open to work'}</span>
          <span className="eyebrow">Full-stack developer</span>
          <h1>{profile.name}</h1>
          <p className="hero-title">{profile.tagline}</p>
          <p className="hero-tagline">{profile.summary}</p>
          <div className="cta-row">
            <Link to="/projects" className="button primary">
              View projects <FaArrowRight />
            </Link>
            <a href={profile.resume || profile.website} className="button secondary" target="_blank" rel="noreferrer">
              Download resume <FaDownload />
            </a>
          </div>
          <div className="social-row">
            <a href={profile.github} target="_blank" rel="noreferrer" aria-label="GitHub">
              <FaGithub />
            </a>
            {profile.linkedin ? (
              <a href={profile.linkedin} target="_blank" rel="noreferrer" aria-label="LinkedIn">
                <FaLinkedin />
              </a>
            ) : null}
            <a href={`mailto:${profile.email}`} aria-label="Email">
              <FaEnvelope />
            </a>
          </div>
        </div>

        <div className="hero-visual">
          <div className="portrait-card">
            <img
              src={profile.avatar || 'https://avatars.githubusercontent.com/u/224866004?v=4'}
              alt={profile.name}
            />
          </div>
        </div>
      </section>

      <section className="content-section page-shell">
        <div className="section-heading">
          <span className="eyebrow">About</span>
          <h2>Designing practical software with a product mindset.</h2>
        </div>
        <div className="about-layout">
          <div>
            <p className="lead-copy">{profile.bio}</p>
            <div className="meta-list">
              <span>{profile.location}</span>
              <span>{profile.education}</span>
            </div>
          </div>
          <div className="info-panel">
            <h3>Primary focus</h3>
            <ul className="focus-list">
              <li><FaCodeBranch /> Django backend engineering</li>
              <li><FaRocket /> AI-powered web applications</li>
              <li><FaArrowRight /> Clean APIs and maintainable product code</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="content-section page-shell">
        <div className="section-heading">
          <span className="eyebrow">Skills</span>
          <h2>Tools, stacks, and strengths.</h2>
        </div>
        <div className="skill-grid">
          {skills.map((group) => (
            <div key={group.label} className="skill-group">
              <h3>{group.label}</h3>
              <div className="tag-list">
                {group.items.map((item) => (
                  <span key={`${group.label}-${item}`} className="chip soft-chip">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="content-section page-shell">
        <div className="section-heading inline-heading">
          <span className="eyebrow">Featured projects</span>
          <Link to="/projects" className="text-link">See all projects</Link>
        </div>
        <div className="card-grid three-up">
          {projects.map((project) => (
            <Link key={project.slug || project.id} to={`/projects/${project.slug}`} className="project-card card">
              <img
                src={project.image_url || project.cover_image || 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=900&q=80'}
                alt={project.title}
              />
              <div className="card-body">
                <span className="chip">{project.category || 'Web'}</span>
                <h3>{project.title}</h3>
                <p>{project.summary || project.short_description || project.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="content-section page-shell">
        <div className="section-heading">
          <span className="eyebrow">Development journey</span>
          <h2>Learning by building.</h2>
        </div>
        <div className="journey-grid">
          {journeySteps.map((step) => (
            <article key={step.title} className="journey-card">
              <div className="journey-index">0{journeySteps.indexOf(step) + 1}</div>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="content-section page-shell">
        <div className="section-heading">
          <span className="eyebrow">Certificates</span>
          <h2>Learning milestones and verified study paths.</h2>
        </div>
        <div className="card-grid three-up">
          {certifications.map((item) => (
            <div key={item.name} className="card cert-card">
              <div className="card-body">
                <span className="chip">{item.status}</span>
                <h3>{item.name}</h3>
                <p>{item.detail}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-banner page-shell">
        <div>
          <p>Ready to build something meaningful?</p>
        </div>
        <Link to="/contact" className="button primary">Start a conversation</Link>
      </section>
    </>
  );
}
