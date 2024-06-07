# home-server
this is just some code i wrote for a home server i have been running off of an old laptop. Running NGINX alongside the flask server provided in this git you can run a simple-ish storage website hosted on the ip of your home server.
# setup
esure you have a laptop running prosumably linux ( arch if possible ) and make sure that nginx is installed
- 1 move to the home dir of your computer with ```cd```
- 2 clone the git repo ```git clone https://github.com/9JH1/home-server```
- 3 add a new socket to your NGINX config in the server portion
  ```
    listen 80;
    listen [::]:80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host  $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-proto $scheme;
        proxy_ssl_verify off;
        client_max_body_size 1000M;
    }
  ```
- 4 run the setup command ```./start.sh```
- 5 run ```ip addr show```, look for you IP address eg ```192.168.68.110``` and type that into a browser on any device connected to the same wifi network as you
