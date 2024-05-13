1. `docker build -t ubuntu_rolling_image .`
2. `docker run -d -it --name ubuntu-rolling -v /home/sonul:/home/ubuntu --user ubuntu ubuntu_rolling_image zsh`
3. `docker exec -it <container_id> zsh`
4. `docker ps -a`
5. `docker stop $(docker ps -q)`
6. `docker rm -f <container_id>`
7. `docker start my_container`
8. `docker run -it --rm --privileged --net=host -e DISPLAY=$DISPLAY -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY -e XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR --name ubuntu-rolling --user=$(id -u):$(id -g) -v /home/sonul/Documents/docker/InsideDocker/home/ubuntu:/home/ubuntu -v /run/user/$(id -u):/run/user/1000 --device /dev/snd:/dev/snd ubuntu_rolling_image zsh`

for running gui apps: `use xhost+`
for running audio do this in docker container: `sudo chown -R 1000:1000 /run/user/1000/*`


   
