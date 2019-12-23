# Nova-PM-sensor-SDS011
## installation:
```
 git clone https://github.com/kissandr/Nova-PM-sensor-SDS011.git
 apt-get install python-serial
```
add to crontab
```
 crontab -e
```
insert as a new line
```
* * * * * flock -w60 /tmp/sds ~/Nova-PM-sensor-SDS011/sds011.py /dev/ttyS0 57 THINGSPEAK_API_KEY
```
Where:

- /dev/ttyS0 : your sensor's serial port
- 57 : read number of samples
- THINGSPEAK_API_KEY : your write key from https://thingspeak.com/

