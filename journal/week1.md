# Week 1 — App Containerization

I containerize the Cruddur App with the procedures below :


## Containerize Backend

I containerized the App Backend as follows

### I installed Python as follows:
```
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
python3 -m flask run --host=0.0.0.0 --port=4567
cd ..
```

I ensured that port  4567 is unlocked on the port tab
I opened the link for port 4567 in a browser and appended `/api/activities/home` to the url.

[]()

### I added Dockerfile to the `backend-flask` directory

```
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```


## Build Container


```docker build -t  backend-flask ./backend-flask```


## Run Container

I ran the container as follows

```
docker run --rm -p 4567:4567 -it backend-flask
FRONTEND_URL="*" BACKEND_URL="*" docker run --rm -p 4567:4567 -it backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
docker run --rm -p 4567:4567 -it  -e FRONTEND_URL -e BACKEND_URL backend-flask
unset FRONTEND_URL="*"
unset BACKEND_URL="*"
```


### I ensured the container is running in the background as follows

`docker container run --rm -p 4567:4567 -d backend-flask`





# Containerize Frontend


I ran NPM Install before building the container to copy the contents of node_modules

```
cd frontend-react-js
npm i 
```

# Create Docker File


I created the Docker file in the  `frontend-react-js` directory as populated it as follows

```
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```

I Built the  Container as follows
`docker build -t frontend-react-js ./frontend-react-js`

##  I ran the Container as follows
`docker run -p 3000:3000 -d frontend-react-js`

# Multiple Containers

## Create a docker-compose file

I created a `docker-compose.yml` at the root directory of the project as follows

````
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
      ```
