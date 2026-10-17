from django.db import models


class Profile(models.Model):
    """Singleton model for the owner's profile information."""
    name = models.CharField(max_length=100, default='Mujahid Islam')
    tagline = models.CharField(max_length=200, default='Full Stack Developer | CSE Student')
    bio = models.TextField(default='')
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    email = models.EmailField(default='mujahidislam2540@gmail.com')
    phone = models.CharField(max_length=20, default='01533827434')
    location = models.CharField(max_length=100, default='Dhaka, Bangladesh')
    github = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')
    twitter = models.URLField(blank=True, default='')
    website = models.URLField(blank=True, default='')
    years_experience = models.PositiveIntegerField(default=0)
    open_to_work = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def save(self, *args, **kwargs):
        # Singleton: only one profile allowed
        if not self.pk and Profile.objects.exists():
            raise ValueError('Only one Profile instance is allowed.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SkillCategory(models.TextChoices):
    FRONTEND = 'frontend', 'Frontend'
    BACKEND = 'backend', 'Backend'
    DATABASE = 'database', 'Database'
    TOOLS = 'tools', 'Tools & DevOps'
    OTHER = 'other', 'Other'


class Skill(models.Model):
    """Technical skill with proficiency level."""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SkillCategory.choices, default=SkillCategory.OTHER)
    proficiency = models.PositiveIntegerField(default=75, help_text='Percentage 0-100')
    icon = models.CharField(max_length=100, blank=True, help_text='Icon name or class, e.g. devicon-python-plain')
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order', 'name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f'{self.name} ({self.category})'


class Project(models.Model):
    """Portfolio project."""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    tech_stack = models.JSONField(default=list, help_text='List of technologies used')
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class Education(models.Model):
    """Educational qualification entry."""
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_year']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'

    def __str__(self):
        return f'{self.degree} — {self.institution}'


class Experience(models.Model):
    """Work or volunteer experience entry."""
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    employment_type = models.CharField(
        max_length=50,
        choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'),
                 ('internship', 'Internship'), ('freelance', 'Freelance'),
                 ('volunteer', 'Volunteer')],
        default='full_time'
    )
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    tech_used = models.JSONField(default=list)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'

    def __str__(self):
        return f'{self.role} at {self.company}'
