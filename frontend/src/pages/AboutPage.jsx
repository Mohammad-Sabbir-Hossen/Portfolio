import { useQuery } from '@tanstack/react-query';
import api from '../api/axios';
import { portfolioProfile, skillGroups as fallbackSkills } from '../data/portfolioData';

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

async function fetchExperiences() {
  const response = await api.get('/experiences/');
  return getArrayData(response.data);
}

async function fetchEducation() {
  const response = await api.get('/education/');
  return getArrayData(response.data);
}

function normalizeSkillGroups(items) {
  if (!items.length) return fallbackSkills;

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

  return [...map.entries()].map(([label, itemList]) => ({ label, items: itemList }));
}

export default function AboutPage() {
  const profileQuery = useQuery({ queryKey: ['profile'], queryFn: fetchProfile });
  const skillsQuery = useQuery({ queryKey: ['skills'], queryFn: fetchSkills });
  const experiencesQuery = useQuery({ queryKey: ['experiences'], queryFn: fetchExperiences });
  const educationQuery = useQuery({ queryKey: ['education'], queryFn: fetchEducation });

  const profile = {
    ...portfolioProfile,
    ...(profileQuery.data || {}),
    name: profileQuery.data?.name || profileQuery.data?.full_name || portfolioProfile.name,
    bio: profileQuery.data?.bio || portfolioProfile.bio,
    email: profileQuery.data?.email || portfolioProfile.email,
    location: profileQuery.data?.location || portfolioProfile.location,
    github: profileQuery.data?.github || profileQuery.data?.github_url || portfolioProfile.github,
    linkedin: profileQuery.data?.linkedin || profileQuery.data?.linkedin_url || portfolioProfile.linkedin,
    website: profileQuery.data?.website || portfolioProfile.website,
  };

  const skills = normalizeSkillGroups(skillsQuery.data || []);
  const experiences = experiencesQuery.data || [];
  const education = educationQuery.data || [];

  return (
    <div className="page-shell content-section about-page">
      <div className="section-heading">
        <span className="eyebrow">About</span>
        <h1>Building practical products with a learning mindset.</h1>
      </div>

      <div className="about-layout">
        <div>
          <p className="lead-copy">{profile.bio}</p>
          <div className="meta-list">
            <span>{profile.location}</span>
            <span>{profile.email}</span>
            <span>{profile.availability || 'Open to work'}</span>
          </div>
        </div>
        <div className="info-panel">
          <h3>Quick profile</h3>
          <ul className="focus-list">
            <li>Focus: Full-stack web development</li>
            <li>Area: Python, Django, React, AI product work</li>
            <li>Education: {profile.education}</li>
          </ul>
        </div>
      </div>

      <div className="sub-section">
        <h2>Technical strengths</h2>
        <div className="skill-grid compact-grid">
          {skills.map((group) => (
            <div key={group.label} className="skill-card">
              <strong>{group.label}</strong>
              <div className="tag-list mini-tags">
                {group.items.map((item) => (
                  <span key={`${group.label}-${item}`} className="chip soft-chip">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="sub-section">
        <h2>Professional journey</h2>
        <div className="timeline vertical">
          {experiences.length ? (
            experiences.map((item) => (
              <div key={item.id} className="timeline-item">
                <div className="timeline-dot" />
                <div>
                  <h3>{item.role}</h3>
                  <p>{item.company}</p>
                  <small>
                    {item.start_date} — {item.is_current ? 'Present' : item.end_date || 'Current'}
                  </small>
                </div>
              </div>
            ))
          ) : (
            <div className="empty-box">Experience details will appear here as they are added.</div>
          )}
        </div>
      </div>

      <div className="sub-section">
        <h2>Education</h2>
        <div className="timeline vertical">
          {education.length ? (
            education.map((item) => (
              <div key={item.id} className="timeline-item">
                <div className="timeline-dot" />
                <div>
                  <h3>{item.degree}</h3>
                  <p>{item.institution}</p>
                  <small>
                    {item.start_year} — {item.end_year || 'Present'}
                  </small>
                </div>
              </div>
            ))
          ) : (
            <div className="empty-box">Education details will appear here as they are added.</div>
          )}
        </div>
      </div>
    </div>
  );
}
