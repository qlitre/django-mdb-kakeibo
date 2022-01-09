# django-mdb-kakeibo

## 概要

Python DjangoとMDB(Material Design for Bootstrap)で作った家計簿アプリです。

## 画面イメージ

### 支出一覧ページ

![image](https://user-images.githubusercontent.com/77523162/148676911-db08e282-9e52-4847-b8f8-8ef4389fc596.png)

### 収入一覧ページ

![image](https://user-images.githubusercontent.com/77523162/148676931-2d2aff61-21c9-40ef-a80e-1aeaff2be070.png)

### 資産一覧ページ
![image](https://user-images.githubusercontent.com/77523162/148676942-a47a81d7-4ad8-44cb-b631-711204bd5f85.png)

### 登録削除

一覧ページからモーダルで追加、削除ができます。

![register](https://user-images.githubusercontent.com/77523162/148681583-ebe96866-0dab-49ee-ab58-942ef234ebcc.gif)

### 月間収支確認ページ

![monthly_balance](https://user-images.githubusercontent.com/77523162/148681657-1b868365-8392-492b-a23c-bf4bba71d9d6.gif)

### 収支推移ページ

収入と支出の月ごとの合計を表示させています。
収入か支出のどちらかだけにしたり、カテゴリごとに表示を切り替えたりできます。

![transition](https://user-images.githubusercontent.com/77523162/148681641-706a8ec4-743d-4192-a543-e7cdd297bd08.gif)

### 資産ダッシュボードページ

登録している日付に応じて月ごとに集計を行っています。
集計の単位は月ごとですが、登録する際は日付単位で行っていきます。

![asset](https://user-images.githubusercontent.com/77523162/148681629-23903e50-6c03-4eec-88ad-3a1242658121.gif)

## つかいかた

まずは適当なディレクトリでgit cloneしてください。

```
git clone https://github.com/qlitre/django-mdb-kakeibo
```

次にcloneしたディレクトリに移動して、仮想環境を立ち上げてください。

```
cd django-mdb-kakeibo
python -m venv myvenv
myvenv\scripts\activate
```

次にライブラリをpip installします。

```
pip install -r requirements.txt
```

installが終わったら、modelをmigrateしてsuperuserを作っておきましょう。

```
python manage.py migrate
python manage.py createsuperuser
```

カテゴリの登録は管理画面から行っていく仕様です。
とりあえずの初期カテゴリデータを用意していますので、動作確認等される際は、お使いください。

```
python manage.py loaddata initial.json
```

settings.pyの以下の項目を環境に合わせて編集ください。

```
# 家計簿のスタート年を定義
# 年の絞り込み検索のスタートする年として使用されます。
KAKEIBO_START_YEAR = 2021

# 家計簿の起算月を定義
# 年初比に使用されます。
MONTH_OF_BEGIN_TERM = 4
```

あとはrunserverして家計簿アプリをお楽しみください。

```
python manage.py runserver
```
