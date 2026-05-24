from node:latest
workdir /usr/local/app

run curl -fsSL https://pi.dev/install.sh | sh
run pi install npm:@lesetong/pi-mimo

workdir /root
copy ./auth.json ./.pi/agent/auth.json

workdir /root/src

entrypoint bash
