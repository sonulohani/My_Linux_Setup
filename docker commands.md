1. `docker build -t ubuntu_rolling_image .`
2. `docker run -d -it --name ubuntu-rolling -v /home/sonul:/home/ubuntu --user ubuntu ubuntu_rolling_image zsh`
3. `docker exec -it <container_id> zsh`
4. `docker ps -a`
5. `docker stop $(docker ps -q)`
6. `docker rm -f <container_id>`
7. `docker start my_container`

   
