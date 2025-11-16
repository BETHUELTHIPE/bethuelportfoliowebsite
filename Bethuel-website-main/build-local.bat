@echo off
echo Building Portfolio locally...
call env\Scripts\activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000