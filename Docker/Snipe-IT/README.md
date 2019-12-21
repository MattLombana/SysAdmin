# Snipe-IT Docker Container

## Starting The Container (Not The First Time)

```
docker-compose up -d
```

## Staring The Container For The First Time

1. Edit `env.local`
2. Run `docker-compose up`
3. You will need to follow the steps necessary to generate the API key for usage in this instance, and you can do so by accessing the shell inside the Snipe-IT container. You can do so with:
```
docker exec -it snipe-it-container-name sh`
```

4. After this you will have shell access to the console and you can generate the app key in the root folder with:
```
php artisan key:generate
```
5. Stop running the docker container

6. After this step, simply replace the <<Fill in Later!>> in your .env file with your actual app key and you are ready to launch the app. Simply run:
```
docker-compose up -d
```
