FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY dist /usr/share/nginx/html

# simulator.html is the site entry point; the editor build stays reachable at /editor.html
RUN mv /usr/share/nginx/html/index.html /usr/share/nginx/html/editor.html

EXPOSE 8000
