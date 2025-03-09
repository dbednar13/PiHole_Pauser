# Pi-hole Pauser

As of Pi-hole V6, the old admin API has been retired and replaced with new REST API endpoints. This is all well and great, but can be a pain if you have less than technical people who need to disable pi-hole every now and then.

The included code creates a docker container with a server. This allows you to bookmark URLs for end users to use for ease of access.

Supports any Pi-hole instance, running on any device on the same network.

# Credit

Most of this code was lifted from Reddit User Va111e as he solved this problem over [in Reddit.](https://www.reddit.com/r/pihole/comments/1ivet3e/how_to_disable_pihole_blocking_via_api_in_v6_via/) I have tweaked the routes to match my own preferences.

# Setup

1. If required, install [Docker](https://docs.docker.com/desktop/)
1. Create an App Password for Pi-hole
   1. Log into Pi-hole
   1. Go to Settings => Web Interface / API
   1. Turn on Expert Mode
   1. Click Configure App Password
1. Checkout code
1. Update `PIHOLE_URL` to point to your Pi-hole server
1. Update `PIHOLE_PASSWORD` to your App Password.
1. In a terminal, navigate to where you checked out the code
1. Run `docker build -t pihole-api .`
1. Run `docker run -d --name pihole-api -p 5000:5000 --restart unless-stopped pihole-api`

# How to Use

Open a browser, navigate to http://\<\<Docker IP Here\>\>:5000/enable or http://\<\<Docker IP Here\>\>:5000/disable

# Reverse Proxy Setup

For users running Pi-hole behind a reverse proxy you can add the new endpoints to your configuration.

## HTTP

Add the 2 location blocks to http routing (if applicable)

```

set $server 192.168.X.Y;

location /enable {
		# Proxy main Pihole traffic
		proxy_pass http://$server:5000/enable;

	}

location /disable {
		# Proxy main Pihole traffic
		proxy_pass http://$server:5000/disable;

	}
```

## HTTPS

For Reverse Proxy with HTTPS

```
set $server 192.168.X.Y;

location /enable {
		# Proxy enable Traffic
		proxy_pass http://$server:5000/enable;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header X-Forwarded-Protocol $scheme;
		proxy_set_header X-Forwarded-Host $http_host;
	}

	location /disable {
		# Proxy disable Traffic
		proxy_pass http://$server:5000/disable;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header X-Forwarded-Protocol $scheme;
		proxy_set_header X-Forwarded-Host $http_host;
	}

```

## Sample

An Advanced Example using subdomain routing where the docker running our pauser and Pi-hole are running on different servers

```
server {
	listen 443 ssl;
	listen [::]:443 ssl;
  http2 on;

	server_name pihole.doman.tld;

	set $pihole 192.168.X.Y;
	set $server 192.168.X.Z;

	location / {
		# Proxy main Pihole traffic
		proxy_pass http://$pihole;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header X-Forwarded-Protocol $scheme;
		proxy_set_header X-Forwarded-Host $http_host;
	}

	location /enable {
		# Proxy Enable Traffic
		proxy_pass http://$server:5000/enable;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header X-Forwarded-Protocol $scheme;
		proxy_set_header X-Forwarded-Host $http_host;
	}

	location /disable {
		# Proxy disable traffic
		proxy_pass http://$server:5000/disable;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header X-Forwarded-Protocol $scheme;
		proxy_set_header X-Forwarded-Host $http_host;
	}

}
```
