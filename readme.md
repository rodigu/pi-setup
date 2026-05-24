# Pi docker image setup

https://stackoverflow.com/questions/41935435/understanding-volume-instruction-in-dockerfile

https://stackoverflow.com/questions/25267372/correct-way-to-detach-from-a-container-without-stopping-it

ctrl+p ctrl+q 

```bash
sudo docker rm pi \
    && sudo docker build -t hiro/pi-llm .\
    && sudo docker run \
        --name=pi -ti \
        -v $(pwd)/pi-volumes/src:/root/src \
        -v $(pwd)/pi-volumes/sessions:/root/.pi/agent/sessions \
        -v $(pwd)/pi-volumes/.pi:/root/src/.pi \
        -v $(pwd)/pi-volumes/skills:/root/.pi/agent/skills \
        hiro/pi-llm
```
