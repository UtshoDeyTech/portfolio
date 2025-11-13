from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('', views.IndexView.as_view(), name='api-index'),

    # Admin Import/Export Views (simple buttons)
    path('admin/portfolio-export/', admin_views.export_portfolio_view, name='admin-portfolio-export'),
    path('admin/portfolio-import/', admin_views.import_portfolio_view, name='admin-portfolio-import'),

    # Education
    path('education/', views.EducationListView.as_view(), name='education-list'),
    path('education/<int:pk>/', views.EducationDetailView.as_view(), name='education-detail'),

    # Experience
    path('experience/', views.ExperienceListView.as_view(), name='experience-list'),
    path('experience/<int:pk>/', views.ExperienceDetailView.as_view(), name='experience-detail'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),

    # Research publications
    path('research/', views.ResearchListView.as_view(), name='research-list'),
    path('research/<slug:slug>/', views.ResearchDetailView.as_view(), name='research-detail'),

    # Research icons
    path('research-icons/', views.ResearchIconListView.as_view(), name='research-icons-list'),

    # Home and Blogs (singletons)
    path('home/', views.HomeDataView.as_view(), name='home-data'),
    path('blogs/', views.BlogsDataView.as_view(), name='blogs-data'),
    path('blog-settings/', views.BlogSettingsView.as_view(), name='blog-settings'),

    # Blog Posts
    path('blog-posts/', views.BlogListView.as_view(), name='blog-list'),
    path('blog-posts/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('trending-blogs/', views.TrendingBlogsView.as_view(), name='trending-blogs'),
    path('featured-blogs/', views.FeaturedBlogsView.as_view(), name='featured-blogs'),
    path('blogs/category/<str:category>/', views.BlogsByCategoryView.as_view(), name='blogs-by-category'),

    # Blog Interactions
    path('blog-posts/<slug:slug>/increment-view/', views.BlogIncrementViewAPIView.as_view(), name='blog-increment-view'),
    path('blog-posts/<slug:slug>/update-duration/', views.BlogUpdateDurationAPIView.as_view(), name='blog-update-duration'),
    path('blog-posts/<slug:slug>/view-stats/', views.BlogViewStatsAPIView.as_view(), name='blog-view-stats'),
    path('blog-posts/<slug:slug>/toggle-like/', views.BlogLikeToggleAPIView.as_view(), name='blog-toggle-like'),
    path('blog-posts/<slug:slug>/comments/', views.BlogCommentCreateAPIView.as_view(), name='blog-comment-create'),
    path('blog-posts/<slug:slug>/comments/list/', views.BlogCommentsListAPIView.as_view(), name='blog-comments-list'),

    # Newsletter
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),

    # Media Files (API endpoints for listing/details)
    path('media-files/', views.MediaFileListView.as_view(), name='media-file-list'),
    path('media-files/<slug:slug>/', views.MediaFileDetailView.as_view(), name='media-file-detail'),

    # CDN endpoint for serving files (secure, not exposing direct file path)
    path('cdn/<slug:slug>/', views.ServeMediaFileView.as_view(), name='serve-media-file'),
]
