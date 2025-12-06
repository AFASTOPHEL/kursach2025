# Берем самый легкий веб-сервер
FROM nginx:alpine

# Удаляем стандартную страницу "Welcome to Nginx"
RUN rm -rf /usr/share/nginx/html/*

# Копируем ТВОИ файлы внутрь контейнера
COPY . /usr/share/nginx/html

# Nginx сам запустится, команду CMD писать не обязательно