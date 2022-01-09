from django.utils import timezone
from datetime import datetime


def common(request):
    """家計簿アプリの共通コンテクスト"""
    now = datetime.now()

    return {"now_year": now.year,
            "now_month": now.month}
