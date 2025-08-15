1. Crear entorno virtual,
- para linux
python -m venv venv

2. Activar entorno virtual
source venv/bin/activate

3. instalar DRF
   pip install djangorestframework

4. instalar librerias
   pip install -r requeriments.txt

5. realizar migraciones
(primero)
python manage.py makemigrations
(segundo)
python manage.py migrate

6. Correr el servidor
python manage.py runserver



