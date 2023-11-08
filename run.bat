@echo off
call .venv\Scripts\activate
@echo off
start chrome http://192.168.0.109:8000/bill
waitress-serve --port=8000 Exellent.wsgi:application
