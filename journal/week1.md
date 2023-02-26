# Week 1 — App Containerization

## Required Homework



I containerize the Cruddur App with the procedures below :


## Containerize Backend

I containerized the App Backend as follows

### I installed Python as follows:
```sh
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
python3 -m flask run --host=0.0.0.0 --port=4567
cd ..
```

- I ensured that port  4567 is unlocked on the port tab
- I opened the link for port 4567 in a browser and appended `/api/activities/home` to the backend url.

![image](https://user-images.githubusercontent.com/50416701/221303330-4b2b20b9-3800-4be6-b62a-d465dc706038.png)

![image](https://user-images.githubusercontent.com/50416701/221303267-e48eb118-33d4-4170-9bf2-7c05725450c1.png)


### I added Dockerfile to the `backend-flask` directory

```dockerfile
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


```sh
docker build -t  backend-flask ./backend-flask
```


## Run Container

I ran the container as follows

```sh
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

```sh
docker container run --rm -p 4567:4567 -d backend-flask
```





# Containerize Frontend


I ran NPM Install before building the container to copy the contents of node_modules

```
cd frontend-react-js
npm i 
```

# Create Docker File


I created the Docker file in the  `frontend-react-js` directory as populated it as follows

```dockerfile
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

```yml
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

![image](https://user-images.githubusercontent.com/50416701/221320812-7bc5e114-cdb5-4eb6-a622-9a0340f491f9.png)





# Adding DynamoDB Local and Postgres

I integrated the following into the existing docker compose file:

 ## Run Postgres Container and Ensure it Works
- Added the following code to my docker-compose file


```yml
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
    
  -  I  installed the postgres client into Gitpod as follows
   
   ```yml
     - name: postgres
    init: |
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
      sudo apt update
      sudo apt install -y postgresql-client-13 libpq-dev
    ```
      
  ### Adding the DynamoDB Local
  - I Added the following code to my docker-compose file

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
    
    ### Proof of Postgres Client and Extension Working

    
    I accessed the postgres database in the command line by running
    
    'psql -Upostgres --host localhost'
    
    ![image](https://user-images.githubusercontent.com/50416701/221320487-345d98fd-b16f-44ea-801c-29c702b481ab.png)



    
    ![image](https://user-images.githubusercontent.com/50416701/221320445-23a23179-0eec-453c-8c86-049dafe57725.png)




    
    
    
    
## Homework Challenges


## Pushing Flask Back-End Image to Docker Hub
- Used `docker login` command to login to my docker hub account. [docker login -u "username" -p "password" docker.io]
- Tag the image `docker tag aws-bootcamp-cruddur-2023-backend-flask:latest dbabarinde/cloud:bootcamp`
- Pushed the image `docker push dbabarinde/cloud:bootcamp`
- Here is the [image url](https://hub.docker.com/r/dbabarinde/cloud) in docker hub.



## Launch EC2 Instance && Pull My Public Flask Image

![dockerpull](https://user-images.githubusercontent.com/50416701/221433679-b8d6a996-cd53-4145-91b6-4c7a2c3ca337.jpg)




## Implement Healthchecks in  GitPod Docker Compose Files
- I added health checks for front-end and backend by adding the code to the Docker compose file

```yml
healthcheck: 
      test: wget --no-verbose --tries=1 --spider https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}/api/activities/home || exit 1
      interval: 20s 
      retries: 2 
      start_period: 20s 
      timeout: 5s 
 ```



 ```yml
 healthcheck:
      test: curl --fail https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST} || exit 1
      interval: 20s
      retries: 2
      start_period: 20s
      timeout: 10s
  ```
