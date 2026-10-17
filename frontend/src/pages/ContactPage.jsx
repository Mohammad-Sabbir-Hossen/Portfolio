import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '../api/axios';

async function submitContact(payload) {
  const response = await api.post('/contact/', payload);
  return response.data;
}

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' });
  const mutation = useMutation({ mutationFn: submitContact });

  const handleChange = (event) => {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    mutation.mutate(form);
  };

  return (
    <div className="page-shell content-section contact-layout">
      <div>
        <span className="eyebrow">Contact</span>
        <h1>Let’s build something meaningful.</h1>
        <p className="lead-copy">Whether you need a product engineer, a design-minded developer, or a collaborator for a new idea, I’d love to hear about it.</p>
      </div>

      <form className="contact-form" onSubmit={handleSubmit}>
        <label>
          Name
          <input name="name" value={form.name} onChange={handleChange} className="text-input" required />
        </label>
        <label>
          Email
          <input type="email" name="email" value={form.email} onChange={handleChange} className="text-input" required />
        </label>
        <label>
          Subject
          <input name="subject" value={form.subject} onChange={handleChange} className="text-input" required />
        </label>
        <label>
          Message
          <textarea name="message" value={form.message} onChange={handleChange} className="text-area" rows="6" required />
        </label>
        <button type="submit" className="button primary" disabled={mutation.isPending}>
          {mutation.isPending ? 'Sending…' : 'Send message'}
        </button>
        {mutation.isSuccess ? <p className="success-message">Your message has been sent successfully.</p> : null}
        {mutation.isError ? <p className="error-message">Something went wrong. Please try again.</p> : null}
      </form>
    </div>
  );
}
