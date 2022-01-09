from django import forms
from .models import PaymentCategory, Payment, Income, IncomeCategory, AssetCategory, Asset
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError


def year_choices():
    """年の選択肢を作成して返す"""
    start_year = settings.KAKEIBO_START_YEAR  # 家計簿の登録を始めた年
    end_year = datetime.now().year
    years = [(year, year) for year in reversed(range(start_year, end_year + 1))]
    years.insert(0, (0, ''))

    return tuple(years)


def month_choices():
    """月の選択肢を作成して返す"""
    months = [(month, str(month).rjust(2, '0')) for month in range(1, 13)]
    months.insert(0, (0, ''))
    return tuple(months)


class PaymentSearchForm(forms.Form):
    """支出検索フォーム"""

    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=year_choices(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm', 'value': ''})
    )

    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=month_choices(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    greater_than = forms.IntegerField(
        label='Greater Than',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'autocomplete': 'off',
                                      'placeholder': 'amount Greater Than'})
    )

    less_than = forms.IntegerField(
        label='Less Than',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'autocomplete': 'off',
                                      'placeholder': 'amount Less Than'})
    )

    key_word = forms.CharField(
        label='検索キーワード',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'autocomplete': 'off',
                                      'placeholder': 'Keyword',
                                      })
    )

    search_category = forms.ModelChoiceField(
        label='カテゴリでの絞り込み',
        required=False,
        queryset=PaymentCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )


class IncomeSearchForm(forms.Form):
    """収入検索フォーム"""
    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=year_choices(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm', 'value': ''})
    )

    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=month_choices(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )


class AssetSearchForm(forms.Form):
    """資産検索フォーム"""
    year = forms.ChoiceField(
        label='年での絞り込み',
        required=False,
        choices=year_choices(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm', 'value': ''})
    )

    month = forms.ChoiceField(
        label='月での絞り込み',
        required=False,
        choices=month_choices(),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    search_category = forms.ModelChoiceField(
        label='カテゴリでの絞り込み',
        required=False,
        queryset=AssetCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )


class PaymentCreateForm(forms.ModelForm):
    """支出登録フォーム"""

    class Meta:
        model = Payment
        fields = '__all__'

        widgets = {
            'date': forms.TextInput(attrs={'autocomplete': 'off',
                                           'placeholder': 'date',
                                           'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.TextInput(attrs={'autocomplete': 'off',
                                             'placeholder': 'amount',
                                             'class': 'form-control'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off',
                                                 'placeholder': 'description',
                                                 'class': 'form-control',
                                                 'rows': '2'}),
        }


class IncomeCreateForm(forms.ModelForm):
    """収入登録フォーム"""

    class Meta:
        model = Income
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'autocomplete': 'off',
                                           'placeholder': 'date',
                                           'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.TextInput(attrs={'autocomplete': 'off',
                                             'placeholder': 'amount',
                                             'class': 'form-control'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off',
                                                 'placeholder': 'description',
                                                 'class': 'form-control',
                                                 'rows': '2'}),
        }


class AssetCreateForm(forms.ModelForm):
    """資産登録フォーム"""

    class Meta:
        model = Asset
        fields = '__all__'

        widgets = {
            'date': forms.TextInput(attrs={'autocomplete': 'off',
                                           'placeholder': 'date',
                                           'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.TextInput(attrs={'autocomplete': 'off',
                                             'placeholder': 'amount',
                                             'class': 'form-control'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off',
                                                 'placeholder': 'description',
                                                 'class': 'form-control',
                                                 'rows': '2'}),
        }


class TransitionGraphSearchForm(forms.Form):
    """推移グラフの絞り込みフォーム"""

    SHOW_CHOICES = (
        ('All', 'All'),
        ('Payment', 'Payment'),
        ('Income', 'Income'),
    )

    payment_category = forms.ModelChoiceField(
        label='支出カテゴリでの絞り込み',
        required=False,
        queryset=PaymentCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )

    income_category = forms.ModelChoiceField(
        label='収入カテゴリでの絞り込み',
        required=False,
        queryset=IncomeCategory.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )

    graph_visible = forms.ChoiceField(required=False,
                                      label='表示グラフ',
                                      choices=SHOW_CHOICES,
                                      widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
                                      )
