from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

# ACCOUNTS VIEWS
from accounts.views import (
    home,
    login_page,
    logout_user,
    profile,
    events,
    ngos,
    dashboard
)

# ACTIVITIES VIEW
from activities.views import activities


urlpatterns = [

    # DJANGO ADMIN PANEL
    path('admin/', admin.site.urls),

    # HOME
    path('', home, name='home'),

    # AUTHENTICATION
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),

    # USER FEATURES
    path('profile/', profile, name='profile'),
    path('activities/', activities, name='activities'),

    # EVENTS
    path('events/', events, name='events'),

    # NGOS
    path('ngos/', ngos, name='ngos'),

    # ADMIN DASHBOARD
    path('dashboard/', dashboard, name='dashboard'),
]


# MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )