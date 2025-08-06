# ref
https://github.com/ckan/ckan-docker/tree/master

# build and run
```
git clone https://github.com/ckan/ckan-docker.git
cd ckan-docker
mv -f .env.example .env
```

## case1
```
mv -f .docker-compose.dev.yml .docker-compose.yml
docker compose build
docker compose up -d
http://localhost:5000
```

## case2
```
docker compose build
docker compose up -d
https://localhost:8443
```

## case3 basic auth
edit nginx/setup/default.conf
```
location / {
    # add start
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd/.htpasswd;
    # add end

}
```

create .htpasswd
```
cd nginx/setup/
htpasswd -cb .htpasswd admin secret123
```

edit nginx/Dockerfile
```
# add start
COPY setup/.htpasswd ${NGINX_DIR}/htpasswd/.htpasswd
# add end
```

start docker
```
docker compose build
docker compose up -d
https://localhost:8443
```

# down
```
docker compose down
```
