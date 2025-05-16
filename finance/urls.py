from django.urls import path
from . import views

urlpatterns = [
    path('financial-report/', views.financial_report, name='finances'),
    path('revenue/add/', views.add_revenue, name='add_revenue'),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('asset/add/', views.add_asset, name='add_asset'),
    path('liability/add/', views.add_liability, name='add_liability'),
    path('cost_of_goods/add/', views.add_cost_of_goods, name='costs-of-goods'),
    
    
    #lists
    path('all-assets/', views.all_assets, name='assets'),
    path('all-liabilities/', views.liabities, name='liabilities'),
    path('all-revenue/', views.revenue, name='revenue'),
    path('all-expense/', views.expense, name='expense'),
    path('all-cost_sales/', views.cost_of_sales, name='cost_sales')
    
]
