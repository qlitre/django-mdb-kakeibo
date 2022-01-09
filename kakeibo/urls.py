from django.urls import path
from . import views

app_name = 'kakeibo'

urlpatterns = [
    path('', views.PaymentList.as_view(), name='payment_list'),
    path('income_list/', views.IncomeList.as_view(), name='income_list'),
    path('asset_list/',views.AssetList.as_view(),name='asset_list'),
    path('payment_create/', views.PaymentCreate.as_view(), name='payment_create'),
    path('income_create/', views.IncomeCreate.as_view(), name='income_create'),
    path('asset_create/', views.AssetCreate.as_view(), name='asset_create'),
    path('payment_delete/<int:pk>/', views.PaymentDelete.as_view(), name='payment_delete'),
    path('income_delete/<int:pk>/', views.IncomeDelete.as_view(), name='income_delete'),
    path('asset_delete/<int:pk>/', views.AssetDelete.as_view(), name='asset_delete'),
    path('monthly_balance/<int:year>/<int:month>/', views.MonthlyBalance.as_view(), name='monthly_balance'),
    path('transition/', views.TransitionView.as_view(), name='transition'),
    path('asset_dashboard/<int:year>/<int:month>/', views.AssetDashboard.as_view(), name='asset_dashboard'),
]
