# Simple messaging application

The application includes the frontend (SPA on Vue.js) and backend (API on Django/DRF).

!!! Both of this parts are included in this repository.

## How to develop • Frontend

1. Go to the `app/frontend` folder and run `npm install` command to install Vue.js libraries.
2. Run `npm run serve` command to start the development server.
3. All the changes in the code would be compiled and hot-reloaded
4. Open your browser `localhost:8080` to see the changes in layout

## How to develop • Backend

1. Install docker-compose (v1.26.0 works)


2. Go to the `*****` folder and run this set of commands:

   ```sh
   $ cp .env.dev_example .env.dev
   $ docker-compose build
   $ docker-compose up -d
   ```
   to copy env file and start containers in detached mode. 
   The backend is available at `localhost:8080`


3. Run the `docker-compose exec web /bin/sh` to run the shell. Then run: 
   ```sh
   $ python manage.py migrate
   $ python manage.py createsuperuser
   ```
   to init database and create admin user. The Django admin is available at 
   `localhost:8080/back/admin`


4.  Use postman to make requests and Django admin to check the result. Run: 
   ```sh
   $ docker-compose logs web
   ```
   to see the Django console logs.


## How to run on production server

1. Install docker-compose (v1.26.0 works)


2. Go to the `app/frontend` folder and run `npm install` command to install Vue.js libraries.


3. Run `npm run build` command to assemble the frontend application.

  
4. Go to the `app` folder and run this commands:

   ```sh
   $ cp .env.dev_prod_example .env.prod
   ```
   to copy env file. Then update the environment variables before starting containers
   

5. Build the images and run the containers in detached mode using:

    ```sh
    $ docker-compose -f prod.yml build
    $ docker-compose -f prod.yml up -d
    ```

6. Run the `docker-compose -f prod.yml exec webp /bin/sh` to run the shell. Then run: 
   ```sh
   $ python manage.py migrate
   $ python manage.py createsuperuser
   $ python manage.py collectstatic
   ```
   to init database, create admin user and collect static files.
   The application is available at `:80` port, use ...`/back/admin` endpoint to enter 
   the Django admin.

7. The link for Postman collection with requests (for production):
   






