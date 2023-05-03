from django.urls import path
from .views import index, RegisterView, profile, edit_profile, Static, LigthNav, Chart, Table, NotFound, Unauthorised, ServerError

urlpatterns = [
    path('', index, name='home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('edit/profile/', edit_profile, name='edit-profile'),
    path('dashboard/layout-static/', Static, name='static'),
    path('dashboard/layout-sidenav-light/', LigthNav, name='light-nav'),
    path('dashboard/chart/', Chart, name='chart'),
    path('dashboard/table/', Table, name='table'),
    path('dashboard/404/', NotFound, name='404'),
    path('dashboard/401/', Unauthorised, name='401'),
    path('dashboard/500/', ServerError, name='500'),

]
