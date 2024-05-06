"""
URL configuration for TestEmail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Emails import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Home, name = "home"),
    path("signup/", views.signup, name = "signup"),
    path("login/", views.signin, name="login"),
    path("get_in/", views.ingreso, name="ingreso"),
    path("youarenotlogged/", views.not_logged, name="not logged"),
    path("logout", views.signout, name="log out"),
    path("undercontract/", views.undercontract, name="under contract"),
    path("tasks/", views.tasks, name="tasks"),
    path("DA/", views.DA, name="DA"),
    path("DA/<int:property_id>/completed/", views.da_completed, name="DA completed"),
    path("DA/<int:property_id>/incompleted/",views.da_incompleted, name="DA incompleted"),
    path("tasks/<int:property_id>/", views.checklist, name="checklist"),
    path("Properties/", views.properties, name="Properties"),
    path("Properties/<int:property_id>/",views.details, name="details"),
    path("properties/<int:property_id>/congratulations/", views.congratulations, name="congrats email"),
    path("Properties/<int:property_id>/closing/", views.closing, name="closing property"),
    path("Properties/<int:property_id>/edit/", views.edit, name="edit property")
    
       
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
