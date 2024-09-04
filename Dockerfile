# base image esto instala la versión de Python para dentro de la imagne Docker. 
# También es la versión de Python que correrá la aplicación en el contenedor.
FROM python:3.11  

# setup environment variable
ENV PYTHONUNBUFFERED=1

# where your code lives  
WORKDIR /app

# Actualiza la versión de pip que se utilizará para instalar las dependencias.
RUN pip install --upgrade pip

COPY ./requirements.txt ./

# run this command to install all dependencies  
RUN pip install -r requirements.txt 

# copy whole project to your docker home directory. 
COPY ./ ./ 

# port where the Django app runs. 
# Esta instrucción es para indicar que la aplicación está corriedo en el puerto 8000
# start server  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]