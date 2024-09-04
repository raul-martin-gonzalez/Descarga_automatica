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

# Instala Chrome y el driver de Chrome
RUN apt-get update && apt-get install -y wget gnupg2
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable
RUN wget -O /tmp/chromedriver.zip 	https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.86/linux64/chromedriver-linux64.zip
RUN apt-get install -y unzip && unzip /tmp/chromedriver.zip -d /usr/local/bin/

# port where the Django app runs. 
# Esta instrucción es para indicar que la aplicación está corriedo en el puerto 8000
# start server  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]