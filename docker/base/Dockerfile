from node:latest

run groupadd -r pi-user && useradd -r -g pi-user -m pi-user

workdir /usr/local/app
run curl -fsSL https://pi.dev/install.sh | sh
run pi install npm:@lesetong/pi-mimo

copy --chown=pi-user:pi-user ./auth.json /home/pi-user/.pi/agent/auth.json

workdir /home/pi-user/src

user pi-user
entrypoint bash
