# Используем официальный образ nginx
FROM nginx:1.27-alpine

# Удаляем дефолтную конфигурацию
RUN rm /etc/nginx/conf.d/default.conf

# Копируем нашу кастомную конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем статические файлы (если нужно)
# Обычно их копирует Django при collectstatic
# COPY /app/static /static

# Указываем, что контейнер слушает порт 80
EXPOSE 80

# Команда запуска
CMD ["nginx", "-g", "daemon off;"]
