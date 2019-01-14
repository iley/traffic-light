Building and flashing
=====================

```bash
mos build --local
mos flash
mos wifi SID PASSWORD
mos aws-iot-setup --aws-iot-thing TrafficLightCloud
```

Once flashed the code can be updated by running
```bash
mos put fs/init.js
```
