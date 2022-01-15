import datetime
from django.views import generic
from .models import Payment, Income, Asset, AssetCategory
from .forms import PaymentSearchForm, IncomeSearchForm, \
    PaymentCreateForm, IncomeCreateForm, AssetCreateForm, \
    TransitionGraphSearchForm, AssetSearchForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from kakeibo import plugins


class PaymentList(generic.ListView):
    """支出一覧ページ"""
    template_name = 'kakeibo/payment_list.html'
    model = Payment
    ordering = '-date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PaymentSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            # yearとmonthにつき何も選択されていないときは0の文字列が入るため、除外
            # forms.pyを参照
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            greater_than = form.cleaned_data.get('greater_than')
            if greater_than:
                queryset = queryset.filter(amount__gte=greater_than)

            less_than = form.cleaned_data.get('less_than')
            if less_than:
                queryset = queryset.filter(amount__lte=less_than)

            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 空白で区切られていた場合は分割して繰り返す、and検索
                for word in key_word.split():
                    queryset = queryset.filter(description__icontains=word)

            category = form.cleaned_data.get('search_category')
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        context['create_form'] = PaymentCreateForm
        context['action_url'] = '/payment_create/'

        return context


class IncomeList(generic.ListView):
    """収入一覧ページ"""
    template_name = 'kakeibo/income_list.html'
    model = Income
    ordering = '-date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        context['create_form'] = IncomeCreateForm
        context['action_url'] = '/income_create/'

        return context


class AssetList(generic.ListView):
    """資産一覧ページ"""
    template_name = 'kakeibo/asset_list.html'
    model = Asset
    ordering = '-date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = AssetSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            category = form.cleaned_data.get('search_category')
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        context['create_form'] = AssetCreateForm
        context['action_url'] = '/asset_create/'

        return context


class PaymentCreate(generic.CreateView):
    """支出登録"""
    model = Payment
    form_class = PaymentCreateForm

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        msg = plugins.success_message_for_item('Register',
                                               'Payment',
                                               payment.date,
                                               payment.category,
                                               payment.amount)
        messages.info(self.request, msg)
        return redirect(self.get_success_url())


class IncomeCreate(generic.CreateView):
    """収入登録"""
    model = Income
    form_class = IncomeCreateForm

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        msg = plugins.success_message_for_item('Register',
                                               'Income',
                                               income.date,
                                               income.category,
                                               income.amount)
        messages.info(self.request, msg)
        return redirect(self.get_success_url())


class AssetCreate(generic.CreateView):
    """資産登録"""
    model = Asset
    form_class = AssetCreateForm

    def get_success_url(self):
        return reverse_lazy('kakeibo:asset_list')

    def post(self, request, *args, **kwargs):
        """同月、同カテゴリが登録されていたらエラーにする"""
        date = request.POST.get('date')
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        year = date.year
        month = date.month
        pk = request.POST.get('category')
        qs_asset = Asset.objects.filter(date__year=year, date__month=month, category=pk)
        if qs_asset.exists():
            category_name = AssetCategory.objects.values().get(pk=pk).get('name')
            msg = f"""
                Failed to register Asset
                Category:{category_name} is already registered in this month
                """
            messages.info(self.request, msg)
            return redirect(self.get_success_url())

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = asset = form.save()
        msg = plugins.success_message_for_item('Register',
                                               'Asset',
                                               asset.date,
                                               asset.category,
                                               asset.amount)
        messages.info(self.request, msg)
        return redirect(self.get_success_url())


class PaymentDelete(generic.DeleteView):
    """支出削除"""
    model = Payment

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def delete(self, request, *args, **kwargs):
        self.object = payment = self.get_object()

        payment.delete()
        msg = plugins.success_message_for_item('Delete',
                                               'Payment',
                                               payment.date,
                                               payment.category,
                                               payment.amount)
        messages.info(self.request, msg)
        return redirect(self.get_success_url())


class IncomeDelete(generic.DeleteView):
    """収入削除"""
    model = Income

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        msg = plugins.success_message_for_item('Delete',
                                               'Income',
                                               income.date,
                                               income.category,
                                               income.amount)
        messages.info(self.request, msg)
        return redirect(self.get_success_url())


class AssetDelete(generic.DeleteView):
    """資産削除"""
    model = Asset

    def get_success_url(self):
        return reverse_lazy('kakeibo:asset_list')

    def delete(self, request, *args, **kwargs):
        self.object = asset = self.get_object()
        asset.delete()
        msg = plugins.success_message_for_item('Delete',
                                               'Asset',
                                               asset.date,
                                               asset.category,
                                               asset.amount)
        messages.info(self.request, msg)

        return redirect(self.get_success_url())


class MonthlyBalance(plugins.MonthlyBalanceMixin, generic.TemplateView):
    """月間収支ページ"""
    template_name = 'kakeibo/monthly_balance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = self.get_monthly_balance_data()
        context.update(data)

        return context


class TransitionView(plugins.BalanceTransitionMixin, generic.TemplateView):
    """月毎の収支推移ページ"""
    template_name = 'kakeibo/balance_transition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.form = form = TransitionGraphSearchForm(self.request.GET or None)
        context['search_form'] = self.form

        data = self.get_balance_transition_data(form)
        context.update(data)

        return context


class AssetDashboard(plugins.AssetDashMixin, generic.TemplateView):
    """資産ダッシュボード"""
    template_name = 'kakeibo/asset_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.get_asset_dash_data()
        context.update(data)
        return context
