
from decimal import Decimal
from django.shortcuts import render, redirect
from .forms import RevenueForm, ExpenseForm, AssetForm, LiabilityForm, Cost_of_SalesForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from calendar import monthrange
from django.contrib import messages
from django.core.paginator import Paginator

from finance.models import Asset, Expense, Liability, Revenue, Cost_of_sales
from django.db.models import Sum

# Create your views here.

# Financial Documents


def get_income_statement(start_date, end_date):
    # Total Revenue
    total_revenue = Revenue.objects.filter(
        date__range=(start_date, end_date)
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Total Expenses
    total_expenses = Expense.objects.filter(
        date__range=(start_date, end_date)
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Total Cost of Sales (COGS)
    total_cost_of_sales = Cost_of_sales.objects.filter(
        date__range=(start_date, end_date)
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Gross Profit = Revenue - COGS
    gross_profit = total_revenue - total_cost_of_sales

    # Net Profit = Gross Profit - Operating Expenses
    net_profit = gross_profit - total_expenses

    return {
        'total_revenue': total_revenue,
        'total_cost_of_sales': total_cost_of_sales,
        'gross_profit': gross_profit,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }

def get_balance_sheet():
    total_assets = Asset.objects.aggregate(Sum('value'))['value__sum'] or 0
    total_liabilities = Liability.objects.aggregate(Sum('amount'))[
        'amount__sum'] or 0
    equity = total_assets - total_liabilities
    return {
        'assets': total_assets,
        'liabilities': total_liabilities,
        'equity': equity
    }


@login_required(login_url='/user/login/')
def financial_report(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    start_date = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    income = get_income_statement(start_date, end_date)
    balance = get_balance_sheet()

    total_revenue = income.get('total_revenue', 0)
    total_expenses = income.get('total_expenses', 0)
    gross_profit = income.get('gross_profit', 0)
    net_profit = income.get('net_profit', 0)

    # Profit Margins
    profit_margin = (net_profit / total_revenue) * \
        100 if total_revenue > 0 else 0
    gross_margin = (gross_profit / total_revenue) * \
        100 if total_revenue > 0 else 0

    # Balance Sheet Ratios
    assets = balance.get('assets', 0)
    liabilities = balance.get('liabilities', 0)
    debt_ratio = (liabilities / assets) * 100 if assets > 0 else 0

    has_data = any([
        total_revenue,
        total_expenses,
        gross_profit,
        net_profit,
        assets,
        liabilities
    ])

    if not has_data:
        messages.error(
            request, f"No financial data found for {start_date.strftime('%B %Y')}.")

    # Recommendations
    recommendations = []
    if net_profit < 0:
        recommendations = [
            "You're running at a net loss. Audit expenses and reassess pricing or revenue strategies."
        ]
    elif gross_margin < 30:
        recommendations = [
            "Your gross margin is low. Consider reducing cost of goods sold or increasing prices."
        ]
    elif total_expenses > (total_revenue * Decimal('0.7')):
        recommendations = [
            "Expenses are high relative to revenue. Look for cost efficiencies."
        ]
    else:
        recommendations = [
            "Financials look healthy. Consider reinvesting in product development or marketing."
        ]

    context = {
        'income': income,
        'balance': balance,
        'profit_margin': profit_margin,
        'gross_margin': gross_margin,
        'debt_ratio': debt_ratio,
        'start_date': start_date,
        'end_date': end_date,
        'recommendations': recommendations,
        'selected_year': year,
        'selected_month': month,
    }

    return render(request, 'financial_summary.html', context)

@login_required(login_url='/user/login/')
def add_cost_of_goods(request):
    form = Cost_of_SalesForm (request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('finances')
    return render(request, 'add_cost_sales.html', {'form':form})

@login_required(login_url='/user/login/')
def add_revenue(request):
    form = RevenueForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('finances')  # Update this if you have a list view
    return render(request, 'add_revenue.html', {'form': form})


@login_required(login_url='/user/login/')
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('finances')
    return render(request, 'add_expense.html', {'form': form})


@login_required(login_url='/user/login/')
def add_asset(request):
    form = AssetForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('finances')
    return render(request, 'add_asset.html', {'form': form})


@login_required(login_url='/user/login/')
def add_liability(request):
    form = LiabilityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('finances')
    return render(request, 'add_liability.html', {'form': form})


@login_required(login_url='/user/login/')
def all_assets(request):
    assets_list = Asset.objects.all()

    return render(request, "assets.html", {"assets_list": assets_list})


@login_required(login_url='/user/login/')
def liabities(request):
    all_liability = Liability.objects.all()

    return render(request, "liability.html", {"all_liability": all_liability})


@login_required(login_url='/user/login/')
def revenue(request):
    # Get selected month and year from query parameters
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Filter by selected month and year if provided
    revenue_list = Revenue.objects.all().order_by('-date')
    if selected_month and selected_year:
        revenue_list = revenue_list.filter(
            date__year=selected_year,
            date__month=selected_month
        )

    # Calculate total amount
    total_revenue = revenue_list.aggregate(total=Sum('amount'))['total'] or 0

    # Pagination
    paginator = Paginator(revenue_list, 10)
    page_number = request.GET.get('page')
    revenue_page = paginator.get_page(page_number)

    # Pass selected filters and total to the template
    context = {
        "revenue_list": revenue_page,
        "total_revenue": total_revenue,
        "selected_month": selected_month,
        "selected_year": selected_year,
    }
    return render(request, "revenue.html", context)


@login_required(login_url='/user/login/')
def expense(request):
    # Get selected month and year from query parameters
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Filter by selected month and year if provided
    expense_list = Expense.objects.all().order_by('-date')
    if selected_month and selected_year:
        expense_list = expense_list.filter(
            date__year=selected_year,
            date__month=selected_month
        )

    # Calculate total amount
    total_expense = expense_list.aggregate(total=Sum('amount'))['total'] or 0

    # Pagination
    paginator = Paginator(expense_list, 10)
    page_number = request.GET.get('page')
    expense_page = paginator.get_page(page_number)

    # Pass selected filters and total to the template
    context = {
        "expense_list": expense_page,
        "total_expense": total_expense,
        "selected_month": selected_month,
        "selected_year": selected_year,
    }
    return render(request, "expense.html", context)





@login_required(login_url='/user/login/')
def cost_of_sales(request):
    # Get selected month and year from query parameters
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # Filter by selected month and year if provided
    cost_list = Cost_of_sales.objects.all().order_by('-date')
    if selected_month and selected_year:
        cost_list = cost_list.filter(
            date__year=selected_year,
            date__month=selected_month
        )

    # Calculate total amount
    total_costs = cost_list.aggregate(total=Sum('amount'))['total'] or 0

    # Pagination
    paginator = Paginator(cost_list, 10)
    page_number = request.GET.get('page')
    cost_page = paginator.get_page(page_number)

    # Pass selected filters and total to the template
    context = {
        "cost_list": cost_page,
        "total_costs": total_costs,
        "selected_month": selected_month,
        "selected_year": selected_year,
    }
    return render(request, "cost_sales.html", context)
