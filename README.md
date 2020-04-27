#### example_shop
#### command for run
#### create project folder
'''
mkdir shop_exampl && cd shop_exampl
git clone https://github.com/Nurzhan097/example_shop.git
'''

#### создание и активация вирт окружения windows
'''
python -m venv env
.\env\Scripts\activate.bat
cd example_shop
pip install -r req.txt
'''

#### запуск django приложения
#### Создание бд и супер пльзователя
'''
manage.py migrate
manage.py createsuperuser
'''
#### заполнить поля (email можно пропустить)

#### запуск суквера
'''
manage.py runserver
'''

