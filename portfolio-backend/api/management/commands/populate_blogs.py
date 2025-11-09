from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import Blog


class Command(BaseCommand):
    help = 'Populate database with dummy blog posts for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy blog posts...')

        # Clear existing blogs (optional)
        Blog.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing blogs'))

        # Blog 1: Featured & Trending Tech Blog
        blog1 = Blog.objects.create(
            slug='getting-started-with-django-rest-framework',
            title='Getting Started with Django REST Framework',
            subtitle='A comprehensive guide to building RESTful APIs with Django',
            excerpt='Learn how to build powerful RESTful APIs using Django REST Framework. This guide covers everything from basic setup to advanced serialization techniques.',
            content_markdown="""# Getting Started with Django REST Framework

Django REST Framework (DRF) is a powerful and flexible toolkit for building Web APIs in Django. In this comprehensive guide, we'll explore how to create professional APIs.

## Why Django REST Framework?

Django REST Framework provides several key benefits:

- **Serialization**: Easily convert complex data types to Python datatypes
- **Authentication**: Built-in support for various auth schemes
- **Viewsets**: Reduce code repetition with viewsets
- **Browsable API**: Interactive API documentation out of the box

## Installation

First, install Django REST Framework using pip:

```bash
pip install djangorestframework
```

## Creating Your First API

Let's create a simple API for a blog application:

```python
from rest_framework import serializers, viewsets
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

## Key Features

### Serializers
Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes.

### ViewSets
ViewSets provide a simple way to handle CRUD operations without writing separate view functions.

### Routers
Routers automatically determine the URL configuration for your API.

## Best Practices

1. **Use ModelSerializers** when working with Django models
2. **Implement proper authentication** for secure APIs
3. **Add pagination** for large datasets
4. **Use filtering** to allow clients to search data
5. **Version your API** to maintain backward compatibility

## Conclusion

Django REST Framework makes it incredibly easy to build robust APIs. Start with the basics and gradually explore advanced features as your application grows.

Happy coding! 🚀
""",
            cover_image='https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800',
            featured_image='https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200',
            category='Web Development',
            tags=['Django', 'Python', 'REST API', 'Backend', 'Tutorial'],
            author='John Developer',
            published_date=timezone.now() - timedelta(days=5),
            views=1250,
            likes=89,
            comments_count=23,
            shares=45,
            is_published=True,
            is_featured=True,
            is_trending=True,
            is_editor_choice=True,
            allow_comments=True,
            display_order=1,
            read_time=8,
            meta_description='Complete guide to Django REST Framework for building powerful APIs',
            meta_keywords='Django, REST Framework, Python, API Development, Tutorial'
        )
        self.stdout.write(self.style.SUCCESS(f'Created: {blog1.title}'))

        # Blog 2: Trending Data Science Blog
        blog2 = Blog.objects.create(
            slug='machine-learning-best-practices-2024',
            title='Machine Learning Best Practices in 2024',
            subtitle='Essential tips and techniques for ML practitioners',
            excerpt='Discover the latest best practices in machine learning, from data preprocessing to model deployment. Learn what works in production environments.',
            content_markdown="""# Machine Learning Best Practices in 2024

The field of machine learning is evolving rapidly. Here are the best practices every ML practitioner should follow in 2024.

## 1. Data Quality First

**Remember**: Garbage in, garbage out!

- Clean your data thoroughly
- Handle missing values appropriately
- Remove outliers (but understand why they exist)
- Ensure proper data normalization

## 2. Feature Engineering

Good features can make or break your model:

| Technique | Use Case | Benefit |
|-----------|----------|---------|
| One-Hot Encoding | Categorical variables | Prevents ordinal assumptions |
| Scaling | Numeric features | Improves convergence |
| Polynomial Features | Non-linear relationships | Captures complexity |

## 3. Model Selection

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Always use cross-validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, X, y, cv=5)
print(f"Accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")
```

## 4. Avoid Overfitting

- Use regularization (L1, L2)
- Implement early stopping
- Keep validation set separate
- Use cross-validation

## 5. Deployment Considerations

1. **Model Versioning**: Track all model versions
2. **Monitoring**: Watch for data drift
3. **A/B Testing**: Test models in production
4. **Scalability**: Plan for growth

## Conclusion

Following these best practices will help you build robust, production-ready ML systems. Stay curious and keep learning!
""",
            cover_image='https://images.unsplash.com/photo-1555255707-c07966088b7b?w=800',
            featured_image='https://images.unsplash.com/photo-1555255707-c07966088b7b?w=1200',
            category='Data Science',
            tags=['Machine Learning', 'AI', 'Best Practices', 'Python', 'Data Science'],
            author='Sarah Chen',
            published_date=timezone.now() - timedelta(days=3),
            views=2890,
            likes=156,
            comments_count=47,
            shares=89,
            is_published=True,
            is_featured=False,
            is_trending=True,
            is_editor_choice=True,
            allow_comments=True,
            display_order=2,
            read_time=12,
            meta_description='Essential machine learning best practices for 2024',
            meta_keywords='Machine Learning, AI, Best Practices, Data Science, Python'
        )
        self.stdout.write(self.style.SUCCESS(f'Created: {blog2.title}'))

        # Blog 3: Featured DevOps Blog
        blog3 = Blog.objects.create(
            slug='docker-kubernetes-beginners-guide',
            title='Docker & Kubernetes: A Beginner\'s Guide',
            subtitle='Containerization and orchestration made simple',
            excerpt='Start your journey into containerization with Docker and Kubernetes. This beginner-friendly guide covers all the basics you need to know.',
            content_markdown="""# Docker & Kubernetes: A Beginner's Guide

Containerization has revolutionized how we deploy applications. Let's explore Docker and Kubernetes from the ground up.

## What is Docker?

Docker is a platform for developing, shipping, and running applications in containers.

### Benefits of Docker

- **Consistency**: Same environment everywhere
- **Isolation**: Applications don't interfere with each other
- **Efficiency**: Lightweight compared to VMs
- **Portability**: Run anywhere Docker is installed

## Your First Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

## Docker Commands Cheat Sheet

```bash
# Build an image
docker build -t myapp:latest .

# Run a container
docker run -p 8000:8000 myapp:latest

# List running containers
docker ps

# Stop a container
docker stop container_id

# Remove a container
docker rm container_id
```

## Introduction to Kubernetes

Kubernetes (K8s) is a container orchestration platform that automates deployment, scaling, and management.

### Key Concepts

- **Pods**: Smallest deployable units
- **Services**: Expose pods to network traffic
- **Deployments**: Manage pod replicas
- **ConfigMaps**: Store configuration data
- **Secrets**: Store sensitive information

## Basic Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8000
```

## Why Use Kubernetes?

- **Auto-scaling**: Scale based on demand
- **Self-healing**: Automatically restart failed containers
- **Load balancing**: Distribute traffic efficiently
- **Rolling updates**: Deploy without downtime

## Next Steps

1. Install Docker Desktop
2. Try minikube for local K8s
3. Deploy a simple application
4. Explore kubectl commands
5. Learn about Helm charts

## Conclusion

Docker and Kubernetes are essential tools in modern DevOps. Start small, practice regularly, and gradually tackle more complex scenarios.
""",
            cover_image='https://images.unsplash.com/photo-1605745341112-85968b19335b?w=800',
            featured_image='https://images.unsplash.com/photo-1605745341112-85968b19335b?w=1200',
            category='DevOps',
            tags=['Docker', 'Kubernetes', 'DevOps', 'Containers', 'Tutorial'],
            author='Mike Johnson',
            published_date=timezone.now() - timedelta(days=7),
            views=1567,
            likes=92,
            comments_count=31,
            shares=56,
            is_published=True,
            is_featured=True,
            is_trending=False,
            is_editor_choice=False,
            allow_comments=True,
            display_order=3,
            read_time=10,
            meta_description='Beginner-friendly guide to Docker and Kubernetes containerization',
            meta_keywords='Docker, Kubernetes, Containers, DevOps, Tutorial'
        )
        self.stdout.write(self.style.SUCCESS(f'Created: {blog3.title}'))

        # Blog 4: Regular Frontend Blog
        blog4 = Blog.objects.create(
            slug='react-hooks-complete-guide',
            title='React Hooks: The Complete Guide',
            subtitle='Master modern React development with hooks',
            excerpt='A deep dive into React Hooks - from useState and useEffect to custom hooks. Everything you need to know to write modern React code.',
            content_markdown="""# React Hooks: The Complete Guide

React Hooks have transformed how we write React components. Let's explore them in detail.

## Why Hooks?

Before hooks, we needed class components for state and lifecycle methods. Hooks let us use these features in functional components.

### Benefits

- Simpler code
- Better code reuse
- Easier testing
- No more `this` keyword confusion

## useState Hook

The most basic hook for adding state:

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

## useEffect Hook

Handle side effects in your components:

```jsx
import { useEffect, useState } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data));
  }, [userId]); // Re-run when userId changes

  return user ? <div>{user.name}</div> : <div>Loading...</div>;
}
```

## Custom Hooks

Create reusable logic:

```jsx
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  const setStoredValue = (newValue) => {
    setValue(newValue);
    localStorage.setItem(key, JSON.stringify(newValue));
  };

  return [value, setStoredValue];
}
```

## Hook Rules

1. Only call hooks at the top level
2. Only call hooks from React functions
3. Custom hooks must start with "use"

## Common Hooks Overview

- **useState**: Add state to components
- **useEffect**: Perform side effects
- **useContext**: Access context values
- **useReducer**: Complex state logic
- **useCallback**: Memoize callbacks
- **useMemo**: Memoize expensive calculations
- **useRef**: Access DOM elements

## Conclusion

Hooks make React development more intuitive and powerful. Start with useState and useEffect, then gradually explore other hooks as needed.
""",
            cover_image='https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800',
            featured_image='https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1200',
            category='Frontend',
            tags=['React', 'JavaScript', 'Hooks', 'Frontend', 'Tutorial'],
            author='Emily Rodriguez',
            published_date=timezone.now() - timedelta(days=2),
            views=987,
            likes=67,
            comments_count=19,
            shares=34,
            is_published=True,
            is_featured=False,
            is_trending=False,
            is_editor_choice=False,
            allow_comments=True,
            display_order=4,
            read_time=9,
            meta_description='Complete guide to React Hooks for modern development',
            meta_keywords='React, Hooks, JavaScript, Frontend, Web Development'
        )
        self.stdout.write(self.style.SUCCESS(f'Created: {blog4.title}'))

        # Blog 5: Recent Cybersecurity Blog
        blog5 = Blog.objects.create(
            slug='web-security-fundamentals-2024',
            title='Web Security Fundamentals for Developers',
            subtitle='Protect your applications from common vulnerabilities',
            excerpt='Learn essential web security practices to protect your applications from common threats like XSS, CSRF, SQL injection, and more.',
            content_markdown="""# Web Security Fundamentals for Developers

Security should be a top priority for every developer. Here are the fundamentals you need to know.

## OWASP Top 10

The OWASP Top 10 represents the most critical security risks:

1. **Broken Access Control**
2. **Cryptographic Failures**
3. **Injection**
4. **Insecure Design**
5. **Security Misconfiguration**

## Common Vulnerabilities

### SQL Injection

**Bad Practice:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

**Good Practice:**
```python
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

### Cross-Site Scripting (XSS)

Always sanitize user input and escape output:

```javascript
// Bad
element.innerHTML = userInput;

// Good
element.textContent = userInput;
// Or use a library like DOMPurify
```

### Cross-Site Request Forgery (CSRF)

Use CSRF tokens for state-changing operations:

```python
# Django provides CSRF protection by default
@csrf_protect
def my_view(request):
    # Your view logic
    pass
```

## Security Best Practices

### Authentication & Authorization

- Use strong password hashing (bcrypt, Argon2)
- Implement multi-factor authentication
- Use JWT or session tokens properly
- Follow principle of least privilege

### Data Protection

- Encrypt sensitive data at rest and in transit
- Use HTTPS everywhere
- Implement proper key management
- Regular security audits

### Input Validation

```python
from django.core.validators import validate_email

def validate_user_input(email, age):
    # Validate email
    validate_email(email)

    # Validate age
    if not (0 < age < 150):
        raise ValueError("Invalid age")
```

## Security Headers

```python
# Django settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
```

## Dependency Management

- Keep dependencies updated
- Use security scanning tools (Snyk, Dependabot)
- Review third-party packages before using

## Conclusion

Security is not a one-time task but an ongoing process. Stay informed about new vulnerabilities and continuously improve your security practices.

Remember: **Security through obscurity is not security!**
""",
            cover_image='https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800',
            featured_image='https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200',
            category='Security',
            tags=['Security', 'Web Development', 'OWASP', 'Best Practices', 'Python'],
            author='Alex Kumar',
            published_date=timezone.now() - timedelta(days=1),
            views=654,
            likes=43,
            comments_count=12,
            shares=28,
            is_published=True,
            is_featured=False,
            is_trending=True,
            is_editor_choice=False,
            allow_comments=True,
            display_order=5,
            read_time=11,
            meta_description='Essential web security fundamentals every developer should know',
            meta_keywords='Web Security, OWASP, Cybersecurity, Development, Best Practices'
        )
        self.stdout.write(self.style.SUCCESS(f'Created: {blog5.title}'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {Blog.objects.count()} dummy blog posts!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write('\nBlog Statistics:')
        self.stdout.write(f'  - Published: {Blog.objects.filter(is_published=True).count()}')
        self.stdout.write(f'  - Trending: {Blog.objects.filter(is_trending=True).count()}')
        self.stdout.write(f'  - Featured: {Blog.objects.filter(is_featured=True).count()}')
        self.stdout.write(f'  - Editor\'s Choice: {Blog.objects.filter(is_editor_choice=True).count()}')
        self.stdout.write(self.style.SUCCESS('\nYou can now test the API endpoints!'))
