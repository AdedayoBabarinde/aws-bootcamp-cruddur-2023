FROM python:3.10-slim-buster

# Inside the container
# Make a new folder inside the container
WORKDIR /backend-flask

# Outside container -> Inside Container
# This contains the libraries we want to install to run the app
COPY requirements.txt requirements.txt

# Inside the container
# install the python libraries used for the app
RUN pip3 install -r requirements.txt

# Outside Container -> Inside Container
# . means everything in the current directory
# first period . - /backend-flask (outside container)
# second period . - /backend-flask (inside container)

COPY . .

# Set environment variable (env vars)
# Inside the container and will remain set while container is running
ENV FLASK_ENV=development

EXPOSE ${PORT}
# CMD (Command)
# python3 -m  flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]