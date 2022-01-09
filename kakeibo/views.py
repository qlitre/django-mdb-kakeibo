import datetime
from django.views import generic
from .models import Payment, PaymentCategory, Income, Asset, AssetCategory
from .forms import PaymentSearchForm, IncomeSearchForm, \
    PaymentCreateForm, IncomeCreateForm, AssetCreateForm, \
    TransitionGraphSearchForm, AssetSearchForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from kakeibo import plugins
from django.db.models import Sum
from django.conf import settings


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
            # 何も選択されていないときは0の文字列が入るため、除外
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
                if key_word:
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
        messages.info(self.request,
                      plugins.success_message_for_item('Register', 'Payment', payment.date, payment.category,
                                                       payment.amount)
                      )
        return redirect(self.get_success_url())


class IncomeCreate(generic.CreateView):
    """収入登録"""
    model = Income
    form_class = IncomeCreateForm

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                      plugins.success_message_for_item('Register', 'Income', income.date, income.category,
                                                       income.amount)
                      )
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
        category_pk = request.POST.get('category')
        if Asset.objects.filter(date__year=year, date__month=month, category=category_pk).exists():
            category_name = AssetCategory.objects.values().get(pk=category_pk).get('name')
            msg = f"""
                Failed to register Asset
                Category:{category_name} is already registered in this month
                """

            messages.info(self.request, msg)
            return redirect(self.get_success_url())

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = asset = form.save()
        messages.info(self.request,
                      plugins.success_message_for_item('Register', 'Asset', asset.date, asset.category,
                                                       asset.amount)
                      )
        return redirect(self.get_success_url())


class PaymentDelete(generic.DeleteView):
    """支出削除"""
    model = Payment

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def delete(self, request, *args, **kwargs):
        self.object = payment = self.get_object()

        payment.delete()
        messages.info(self.request,
                      plugins.success_message_for_item('Delete', 'Payment', payment.date, payment.category,
                                                       payment.amount)
                      )
        return redirect(self.get_success_url())


class IncomeDelete(generic.DeleteView):
    """収入削除"""
    model = Income

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        messages.info(self.request,
                      plugins.success_message_for_item('Delete', 'Income', income.date, income.category,
                                                       income.amount)
                      )
        return redirect(self.get_success_url())


class AssetDelete(generic.DeleteView):
    """資産削除"""
    model = Asset

    def get_success_url(self):
        return reverse_lazy('kakeibo:asset_list')

    def delete(self, request, *args, **kwargs):
        self.object = asset = self.get_object()
        asset.delete()
        messages.info(self.request,
                      plugins.success_message_for_item('Delete', 'Asset', asset.date, asset.category,
                                                       asset.amount)
                      )
        return redirect(self.get_success_url())


class MonthlyBalance(generic.TemplateView):
    """月間収支ページ"""
    template_name = 'kakeibo/monthly_balance.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['year_month'] = datetime.datetime(year=year, month=month, day=1)
        context = plugins.add_prev_and_next_month_year_to_context(context, year, month)

        queryset = Payment.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # 後の工程でエラーになるため、クエリセットが何もない時はcontextを返す
        if not queryset:
            return context

        df_payment = read_frame(queryset,
                                fieldnames=['category', 'amount'])

        df_payment_pivot = pd.pivot_table(df_payment, index='category', values='amount', aggfunc=np.sum)
        payment_categories = list(df_payment_pivot.index.values)
        payment_values = [val[0] for val in df_payment_pivot.values]
        context['categories'] = payment_categories
        context['payments_of_category'] = payment_values

        # 支出テーブルを作成する
        payment_dict = {}
        total_payment = df_payment['amount'].sum()
        for category, amount in zip(payment_categories, payment_values):
            composition_ratio = round(100 * (amount / total_payment), 2)
            payment_dict[category] = {'amount': amount, 'composition_ratio': composition_ratio}

        context['table_set'] = payment_dict
        context['total_payment'] = total_payment

        # 総収入
        total_income = Income.objects.filter(date__year=year, date__month=month).aggregate(Sum('amount'))['amount__sum']
        context['total_income'] = total_income

        # 収支
        if total_income:
            context['diff'] = total_income - total_payment
        context = plugins.add_colormap_to_context(context=context,
                                                  queryset=PaymentCategory.objects.all(),
                                                  graph_labels=payment_categories)

        return context


class TransitionView(generic.TemplateView):
    """月毎の収支推移ページ"""
    template_name = 'kakeibo/transition.html'

    def get_context_data(self, **kwargs):
        def get_amount(_queryset, _labels):
            """年月に対応するamountをyieldして返す"""
            _df = read_frame(_queryset,
                             fieldnames=['date', 'amount'])
            _df['date'] = pd.to_datetime(_df['date'])
            _df['month'] = _df['date'].dt.strftime('%Y-%m')
            _dict_from_df = pd.pivot_table(_df, index='month', values='amount', aggfunc=np.sum).to_dict()['amount']
            for _label in _labels:
                yield _dict_from_df.get(_label, 0)

        context = super().get_context_data(**kwargs)
        self.form = form = TransitionGraphSearchForm(self.request.GET or None)
        context['search_form'] = self.form
        payment_queryset = Payment.objects.all()
        income_queryset = Income.objects.all()

        graph_visible = None

        # とりあえず支出モデルを元にラベルを作る
        df = read_frame(payment_queryset,
                        fieldnames=['date'])
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.strftime('%Y-%m')
        df = df.drop_duplicates(subset='month')
        labels = list(df['month'].values)
        context['labels'] = labels

        if form.is_valid():
            payment_category = form.cleaned_data.get('payment_category')
            if payment_category:
                payment_queryset = payment_queryset.filter(category=payment_category)
            income_category = form.cleaned_data.get('income_category')
            if income_category:
                income_queryset = income_queryset.filter(category=income_category)

            graph_visible = form.cleaned_data.get('graph_visible')

        # forms.pyで表示グラフ名を定義
        if graph_visible == 'All':
            if payment_queryset:
                context['payments'] = [amount for amount in get_amount(payment_queryset, labels)]
            if income_queryset:
                context['incomes'] = [amount for amount in get_amount(income_queryset, labels)]

        if not graph_visible or graph_visible == 'Payment':
            if payment_queryset:
                context['payments'] = [amount for amount in get_amount(payment_queryset, labels)]

        if not graph_visible or graph_visible == 'Income':
            if income_queryset:
                context['incomes'] = [amount for amount in get_amount(income_queryset, labels)]

        return context


class AssetDashboard(generic.TemplateView):
    """資産ダッシュボード"""
    template_name = 'kakeibo/asset_dashboard.html'

    def get_context_data(self, **kwargs):
        def calc_diff_ratio(now_amount, past_amount):
            if not now_amount and not past_amount:
                return None
            if not now_amount:
                return -100.0
            elif not past_amount:
                return None
            else:
                return round(100 * (now_amount / past_amount - 1), 2)

        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['year_month'] = datetime.datetime(year=year, month=month, day=1)
        context = plugins.add_prev_and_next_month_year_to_context(context, year, month)
        queryset_all = Asset.objects.all()
        if not queryset_all:
            return context
        df_all = read_frame(qs=queryset_all,
                            fieldnames=['date', 'amount', 'category'])
        df_all['date'] = pd.to_datetime(df_all['date'])
        df_all['month'] = df_all['date'].dt.strftime('%Y-%m')
        df_all_pivot = pd.pivot_table(df_all, index='month', values='amount', aggfunc=np.sum).fillna(0)
        df_all_pivot['diff'] = df_all_pivot['amount'].pct_change().fillna(0)
        context['months'] = list(df_all_pivot.index.values)
        context['amounts'] = [val[0] for val in df_all_pivot.values]
        context['spark_values'] = [val * 100 for val in df_all_pivot['diff'].values]

        queryset_now_month = Asset.objects.filter(date__year=year, date__month=month)
        if not queryset_now_month:
            return context

        df_now_month = read_frame(queryset_now_month,
                                  fieldnames=['amount', 'category'])
        # アセットアロケーショングラフの作成
        df_pivot_now = pd.pivot_table(df_now_month, index='category', values='amount', aggfunc=np.sum)
        donut_labels = list(df_pivot_now.index.values)
        donut_values = [val[0] for val in df_pivot_now.values]
        context['donut_labels'] = donut_labels
        context['donut_prices'] = donut_values

        # カテゴリに対応したカラーマップをつくる
        context = plugins.add_colormap_to_context(context=context,
                                                  queryset=AssetCategory.objects.all(),
                                                  graph_labels=donut_labels)

        # テーブルの作成
        df_prev_month = read_frame(qs=Asset.objects.filter(date__year=context['prev_year'],
                                                           date__month=context['prev_month']),
                                   fieldnames=['amount', 'category'])
        df_prev_month = df_prev_month.rename(columns={'amount': 'amount_prev_month'})
        begin_term_month = settings.MONTH_OF_BEGIN_TERM
        begin_term_year = year - 1 if month < begin_term_month else year
        df_begin_term = read_frame(qs=Asset.objects.filter(date__year=begin_term_year,
                                                           date__month=begin_term_month),
                                   fieldnames=['amount', 'category'])
        df_begin_term = df_begin_term.rename(columns={'amount': 'amount_begin_term'})

        df_merge = pd.merge(df_now_month, df_prev_month, on='category', how='outer')
        df_merge = pd.merge(df_merge, df_begin_term, on='category', how='outer').fillna(0)
        df_merge = df_merge.astype({'amount': int,
                                    'amount_prev_month': int,
                                    'amount_begin_term': int})
        df_merge = df_merge.sort_values('category')

        total_amount_now = df_now_month['amount'].sum()
        total_amount_prev_month = df_prev_month['amount_prev_month'].sum()
        total_amount_begin_term = df_begin_term['amount_begin_term'].sum()
        dic = {}
        for val in df_merge[['category', 'amount', 'amount_prev_month', 'amount_begin_term']].values:
            category = val[0]
            amount_now = val[1]
            amount_prev_month = val[2]
            amount_begin_term = val[3]
            dic[category] = {
                'now': amount_now,
                'prev_month': amount_prev_month,
                'diff_prev_month': amount_now - amount_prev_month,
                'diff_ratio_prev_month': calc_diff_ratio(amount_now, amount_prev_month),
                'begin_term': amount_begin_term,
                'diff_begin_term': amount_now - amount_begin_term,
                'diff_ratio_begin_term': calc_diff_ratio(amount_now, amount_begin_term),
                'composition_ratio': round(100 * (amount_now / total_amount_now), 1),
            }

        context['table_set'] = dic
        context['total'] = {
            'now': total_amount_now,
            'prev_month': total_amount_prev_month,
            'diff_prev_month': total_amount_now - total_amount_prev_month,
            'diff_ratio_prev_month': calc_diff_ratio(total_amount_now, total_amount_prev_month),
            'begin_term': total_amount_begin_term,
            'diff_begin_term': total_amount_now - total_amount_begin_term,
            'diff_ratio_begin_term': calc_diff_ratio(total_amount_now, total_amount_begin_term)
        }

        return context
