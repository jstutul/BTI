from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('',home,name='home'),
    path("verify/", verify_certificate, name="verify_certificate"),
    path("courses/", courses_view, name="courses_view"),
    path("centers/", trainning_center, name="trainning_center"),
    path("trems/", trems_condition, name="trems_condition"),
    path("privacy/", privacy_view, name="privacy_view"),
    path("contact/", contact_us, name="contact_us"),
    path('verify/idcard/<int:pk>/', id_card, name='id_card'),
    path('verify/admit/<int:pk>/', admit_card, name='admit_card'),
    path('verify/registercard/<int:pk>/', register_card, name='register_card'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
