upstream backend {
    server pomidorka.com:8000 max_fails=3;
}

server {
	listen 80;
	listen [::]:80;

    server_name pomidorka.com www.pomidorka.com;

	location / {
	    root /home/zogovaleksandr/pomidorka/public;
	}

    location /api/ {
	    proxy_pass http://backend;
	}
}
