"""
Management command to seed the database with demo data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.portfolio.models import Profile, Skill, Project, Education, Experience
from apps.blog.models import Category, Tag, BlogPost
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with demo data for Mujahid Islam portfolio'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Seeding database...'))

        # ── Owner user ──────────────────────────────────────────────────────────
        if not User.objects.filter(email='mujahidislam2540@gmail.com').exists():
            owner = User.objects.create_superuser(
                email='mujahidislam2540@gmail.com',
                username='mujahid',
                password='admin1234',
                first_name='Mujahid',
                last_name='Islam',
                is_owner=True,
            )
            self.stdout.write(self.style.SUCCESS('  Created owner user: mujahidislam2540@gmail.com / admin1234'))
        else:
            owner = User.objects.get(email='mujahidislam2540@gmail.com')
            self.stdout.write('  Owner user already exists.')

        # ── Profile ─────────────────────────────────────────────────────────────
        if not Profile.objects.exists():
            Profile.objects.create(
                name='Mujahid Islam',
                tagline='Full Stack Developer | CSE Student at DIU',
                bio=(
                    'I am Mujahid Islam, a passionate Computer Science & Engineering student '
                    'at Dhaka International University, currently in my 5th semester. '
                    'I love learning modern web technologies and Artificial Intelligence. '
                    'My dream is to become a skilled Full Stack Developer and build '
                    'AI-powered web applications. I enjoy solving programming problems '
                    'and creating beautiful, responsive websites.'
                ),
                email='mujahidislam2540@gmail.com',
                phone='01533827434',
                location='Dhaka, Bangladesh',
                years_experience=1,
                open_to_work=True,
            )
            self.stdout.write(self.style.SUCCESS('  Created profile'))
        else:
            self.stdout.write('  Profile already exists.')

        # ── Skills ──────────────────────────────────────────────────────────────
        skills_data = [
            ('HTML5', 'frontend', 85, 0),
            ('CSS3', 'frontend', 80, 1),
            ('Responsive Design', 'frontend', 78, 2),
            ('React', 'frontend', 65, 3),
            ('Python', 'backend', 80, 0),
            ('Django', 'backend', 72, 1),
            ('Django REST Framework', 'backend', 65, 2),
            ('SQL', 'database', 75, 0),
            ('PostgreSQL', 'database', 65, 1),
            ('SQLite', 'database', 80, 2),
            ('Git', 'tools', 75, 0),
            ('GitHub', 'tools', 75, 1),
            ('VS Code', 'tools', 90, 2),
            ('Vite', 'tools', 60, 3),
        ]
        for name, cat, prof, order in skills_data:
            Skill.objects.get_or_create(name=name, defaults={
                'category': cat, 'proficiency': prof, 'order': order
            })
        self.stdout.write(self.style.SUCCESS(f'  Created {len(skills_data)} skills'))

        # ── Projects ────────────────────────────────────────────────────────────
        projects_data = [
            {
                'title': 'Full Stack Portfolio & Blog',
                'slug': 'fullstack-portfolio-blog',
                'description': (
                    'A complete full-stack portfolio and blog application built with Django REST Framework '
                    'on the backend and React 18 + Vite on the frontend. Features JWT authentication, '
                    'blog with comment moderation, contact form, admin dashboard, and responsive design '
                    'with dark/light theme toggle.'
                ),
                'short_description': 'Full-stack portfolio + blog with Django DRF & React 18',
                'tech_stack': ['Python', 'Django', 'DRF', 'React', 'Vite', 'JWT', 'SQLite'],
                'status': 'completed',
                'is_featured': True,
                'order': 0,
            },
            {
                'title': 'Portfolio Website',
                'slug': 'portfolio-website',
                'description': (
                    'A responsive personal portfolio website built with HTML5 and CSS3. '
                    'Features a clean, modern design with smooth scrolling and mobile-first layout. '
                    'Showcases projects, skills, education, and contact information.'
                ),
                'short_description': 'Responsive personal portfolio with HTML & CSS',
                'tech_stack': ['HTML5', 'CSS3', 'Responsive Design'],
                'status': 'completed',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Django Blog Application',
                'slug': 'django-blog-application',
                'description': (
                    'A full-featured blog application built with Django and PostgreSQL. '
                    'Features user authentication, post categories, tags, comments, '
                    'and an admin panel for content management.'
                ),
                'short_description': 'Blog app with Django & PostgreSQL',
                'tech_stack': ['Python', 'Django', 'PostgreSQL', 'HTML', 'CSS'],
                'status': 'completed',
                'is_featured': False,
                'order': 2,
            },
            {
                'title': 'Multi-Vendor E-commerce Database',
                'slug': 'multi-vendor-ecommerce-db',
                'description': (
                    'Designed a complete E-commerce Multi Vendor database schema using ER Diagram. '
                    'Covers entities for vendors, products, orders, customers, payments, and reviews. '
                    'Implemented with PostgreSQL.'
                ),
                'short_description': 'E-commerce multi-vendor DB design with ER Diagram',
                'tech_stack': ['PostgreSQL', 'ER Diagram', 'SQL'],
                'status': 'completed',
                'is_featured': False,
                'order': 3,
            },
            {
                'title': 'Book API',
                'slug': 'book-api',
                'description': (
                    'A RESTful API for managing a book catalogue built with Django REST Framework. '
                    'Supports CRUD operations, filtering, search, and pagination. '
                    'Includes token authentication.'
                ),
                'short_description': 'RESTful Book API with DRF',
                'tech_stack': ['Python', 'Django', 'DRF', 'SQLite'],
                'status': 'completed',
                'is_featured': False,
                'order': 4,
            },
        ]
        for data in projects_data:
            Project.objects.get_or_create(slug=data['slug'], defaults=data)
        self.stdout.write(self.style.SUCCESS(f'  Created {len(projects_data)} projects'))

        # ── Education ───────────────────────────────────────────────────────────
        education_data = [
            {
                'degree': 'B.Sc. in Computer Science & Engineering',
                'institution': 'Dhaka International University',
                'field_of_study': 'Computer Science & Engineering',
                'start_year': '2023',
                'end_year': '2027',
                'grade': 'Running',
                'is_current': True,
                'order': 0,
            },
            {
                'degree': 'Higher Secondary Certificate (HSC)',
                'institution': 'Kurigram Government College',
                'field_of_study': 'Science',
                'start_year': '2020',
                'end_year': '2022',
                'grade': 'Completed',
                'is_current': False,
                'order': 1,
            },
            {
                'degree': 'Secondary School Certificate (SSC)',
                'institution': 'Alia Kamil Madrasha, Kurigram',
                'field_of_study': 'Science',
                'start_year': '2018',
                'end_year': '2020',
                'grade': 'Completed',
                'is_current': False,
                'order': 2,
            },
        ]
        for data in education_data:
            Education.objects.get_or_create(
                degree=data['degree'], institution=data['institution'],
                defaults=data
            )
        self.stdout.write(self.style.SUCCESS(f'  Created {len(education_data)} education entries'))

        # ── Blog Categories & Tags ──────────────────────────────────────────────
        categories = ['Python', 'Django', 'React', 'Web Development', 'CSS', 'Career']
        for name in categories:
            Category.objects.get_or_create(name=name)

        tags_data = ['tutorial', 'beginner', 'django-rest', 'react-hooks', 'portfolio', 'css-tips', 'python-tips']
        for name in tags_data:
            Tag.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f'  Created categories and tags'))

        # ── Blog Posts ─────────────────────────────────────────────────────────
        python_cat = Category.objects.get(name='Python')
        django_cat = Category.objects.get(name='Django')
        react_cat = Category.objects.get(name='React')
        webdev_cat = Category.objects.get(name='Web Development')

        posts_data = [
            {
                'title': 'Getting Started with Django REST Framework',
                'slug': 'getting-started-with-django-rest-framework',
                'category': django_cat,
                'excerpt': 'Learn how to build powerful REST APIs with Django REST Framework from scratch.',
                'content': '''# Getting Started with Django REST Framework

Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django.

## Installation

```bash
pip install djangorestframework
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    "corsheaders",
    'rest_framework',
]
```

## Your First Serializer

```python
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

## Creating a ViewSet

```python
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

## Routing

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books', BookViewSet)
```

DRF makes building APIs extremely fast and maintainable!
''',
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'Building Your First React App with Vite',
                'slug': 'building-your-first-react-app-with-vite',
                'category': react_cat,
                'excerpt': 'Vite is an incredibly fast build tool. Let us create a React app from scratch.',
                'content': '''# Building Your First React App with Vite

Vite is a next-generation frontend build tool that is much faster than Create React App.

## Setup

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

## Project Structure

```
my-app/
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
└── vite.config.js
```

## Your First Component

```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>;
}

export default Greeting;
```

Vite's Hot Module Replacement (HMR) makes development extremely fast!
''',
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'CSS Tips Every Developer Should Know',
                'slug': 'css-tips-every-developer-should-know',
                'category': webdev_cat,
                'excerpt': 'Master these CSS techniques to build beautiful, responsive websites.',
                'content': '''# CSS Tips Every Developer Should Know

## 1. Use CSS Custom Properties (Variables)

```css
:root {
  --primary-color: #00ff88;
  --bg-color: #0d0f12;
  --font-body: 'Inter', sans-serif;
}

body {
  background: var(--bg-color);
  color: var(--primary-color);
  font-family: var(--font-body);
}
```

## 2. Flexbox for Layouts

```css
.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
```

## 3. CSS Grid for Complex Layouts

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

## 4. Smooth Animations

```css
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 255, 136, 0.2);
}
```

These techniques will make your websites look professional!
''',
                'status': 'published',
                'is_featured': False,
            },
            {
                'title': 'Why I Chose Python as My First Programming Language',
                'slug': 'why-i-chose-python-first-language',
                'category': python_cat,
                'excerpt': 'Python is an excellent choice for beginners. Here is why I started with Python.',
                'content': '''# Why I Chose Python as My First Programming Language

When I started learning programming, I had many choices: C, Java, JavaScript, Python...

## Why Python?

### 1. Readable Syntax
Python reads like English. Compare:

```python
# Python
numbers = [1, 2, 3, 4, 5]
squares = [n**2 for n in numbers]
print(squares)  # [1, 4, 9, 16, 25]
```

### 2. Versatile
You can use Python for:
- Web development (Django, Flask)
- Data Science (Pandas, NumPy)
- Machine Learning (TensorFlow, PyTorch)
- Automation

### 3. Great Community
Python has one of the largest communities, meaning tons of tutorials, packages, and help.

## My Python Journey

I started with basic syntax, then moved to Django for web development. 
Python opened the door to full-stack development for me!

If you are just starting out, I highly recommend Python.
''',
                'status': 'published',
                'is_featured': False,
            },
            {
                'title': 'Draft: Advanced React Patterns',
                'slug': 'draft-advanced-react-patterns',
                'category': react_cat,
                'excerpt': 'Coming soon: advanced patterns for React applications.',
                'content': 'This post is still being written...',
                'status': 'draft',
                'is_featured': False,
            },
        ]

        for data in posts_data:
            slug = data.pop('slug')
            if not BlogPost.objects.filter(slug=slug).exists():
                post = BlogPost.objects.create(
                    slug=slug,
                    author=owner,
                    published_at=timezone.now() if data.get('status') == 'published' else None,
                    **data
                )
                # Add tags
                if 'tutorial' in slug or 'getting-started' in slug:
                    tag, _ = Tag.objects.get_or_create(name='tutorial')
                    post.tags.add(tag)
        self.stdout.write(self.style.SUCCESS(f'  Created blog posts'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('  Login credentials:')
        self.stdout.write('    Email:    mujahidislam2540@gmail.com')
        self.stdout.write('    Password: admin1234')
        self.stdout.write('')
        self.stdout.write('  IMPORTANT: Change the password after first login!')
