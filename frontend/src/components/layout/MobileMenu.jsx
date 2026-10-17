import { NavLink } from 'react-router-dom';

export default function MobileMenu({ isOpen, items, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="mobile-menu" role="dialog" aria-modal="true">
      <nav>
        {items.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => (isActive ? 'mobile-link active' : 'mobile-link')}
            onClick={onClose}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
