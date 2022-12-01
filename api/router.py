from django.urls import path, include


urlpatterns = [
    path('summaries/', include('api.views.summary.urls')),
    path('companies/', include('api.views.company.urls')),
    path('transactions/', include('api.views.transaction.urls')),
]
