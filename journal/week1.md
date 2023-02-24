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

I ensured that i can orchestrate multiple containers to run side by side as follows

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

To verify if the notification feature is active, i ensured that port 3000 and 4567 are open,
and opened the frontend url in a browser as follows

![image](https://user-images.githubusercontent.com/50416701/221268154-f688eb1d-acd8-43cc-9ddf-ec0925c649fd.png)



# Adding DynamoDB Local and Postgres

I integrated the following into the existing docker compose file:

## Postgres

```
services:
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
volumes:
  db:
    driver: local
    ```
    
   I  installed the postgres client into Gitpod as follows
   
   ```
     - name: postgres
    init: |
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
      sudo apt update
      sudo apt install -y postgresql-client-13 libpq-dev
      ```
      
      
      Adding the DynamoDB Local
      
      services:
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
    
    ## Proof of Postgres Client and Extension Working

    
    I accessed the postgres database in the command line by running
    
    ```
    psql -Upostgres --host localhost
    ```
    
    ![image](https://user-images.githubusercontent.com/50416701/221267926-82fa83a2-ce8e-401a-a3f4-76f204118cb1.png)


    
    ![image](https://user-images.githubusercontent.com/50416701/221267805-35671783-f759-44fc-9ccb-7bcf3113a3a1.png)



    
    
    
    
    #Homework Challenges
