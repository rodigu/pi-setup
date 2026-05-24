# Pi docker image setup

https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile

https://stackoverflow.com/questions/25267372/correct-way-to-detach-from-a-container-without-stopping-it

ctrl+p ctrl+q

```bash
sudo docker build -t rodigu/pi-base docker/base \
&& sudo docker build -t rodigu/pi-read docker/read \
&& sudo docker build -t rodigu/pi-edit docker/edit
```

```bash
sudo docker run \
    --name=pi-edit -ti \
    -v $(pwd)/src:/root/src \
    -v $(pwd)/sessions:/root/.pi/agent/sessions \
    -v /home/hiroto/dev/pi-setup/pi-volumes/.pi:/root/src/.pi \
    -v /home/hiroto/dev/pi-setup/pi-volumes/skills:/root/.pi/agent/skills \
    rodigu/pi-edit
```
