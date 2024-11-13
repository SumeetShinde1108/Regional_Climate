from django.contrib import admin
from django.urls import path
from regional_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weatherdata/', views.WeatherDataView.as_view(), name='monthly-data-list'),
    path('years/',views.get_years,name='years'),
    path('parameters/',views.get_parameters, name='parameters'),
    path('regions/',views.get_regions,name='regions'),
    path('createdata/',views.WeatherDataCreateView.as_view(),name='create-data'),
    path('analyticaldata/',views.WeatherAnalyticsView.as_view(), name='analytical-data'),
    path('', views.home, name='home'),
    path('weather-data/', views.weather_data, name='weather_data'),
    path('weather-analysis/',views.analytical_data,name='weather-analysis')
]


