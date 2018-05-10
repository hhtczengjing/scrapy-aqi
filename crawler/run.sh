#!/bash
. /etc/profile
. ~/.bash_profile
cd /home/aqi
docker run --rm zengjing/pm25:1.0.0
