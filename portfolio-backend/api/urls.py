from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='api-index'),

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

    # Blog Posts
    path('blog-posts/', views.BlogListView.as_view(), name='blog-list'),
    path('blog-posts/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('trending-blogs/', views.TrendingBlogsView.as_view(), name='trending-blogs'),
    path('featured-blogs/', views.FeaturedBlogsView.as_view(), name='featured-blogs'),
    path('blogs/category/<str:category>/', views.BlogsByCategoryView.as_view(), name='blogs-by-category'),

    # Blog Interactions
    path('blog-posts/<slug:slug>/increment-view/', views.BlogIncrementViewAPIView.as_view(), name='blog-increment-view'),
    path('blog-posts/<slug:slug>/toggle-like/', views.BlogLikeToggleAPIView.as_view(), name='blog-toggle-like'),
    path('blog-posts/<slug:slug>/comments/', views.BlogCommentCreateAPIView.as_view(), name='blog-comment-create'),
    path('blog-posts/<slug:slug>/comments/list/', views.BlogCommentsListAPIView.as_view(), name='blog-comments-list'),
]
