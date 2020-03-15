from django.contrib import admin
from django.urls import path, include
from app.views import PostList, PostDetail, SignUpView, UserDetail, SearchView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostList.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('search/', SearchView.as_view(), name='search'),
]

urlpatterns += (
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
