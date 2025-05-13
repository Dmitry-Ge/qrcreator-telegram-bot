1. Take TelegramAPI TOKEN , use @BotFather
2. Build docker container
   ```docker build -t qrcode_bot .```
4. Rundocker container with TOKEN variable
   ```docker run -e "TOKEN=xxx:zzz" -d --rm --name QRCodeBot qrcode_bot```
5. Check comtainer's logs
   ```docker logs -f QRCodeBot```
