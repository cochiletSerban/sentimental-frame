### Done

Basic features

- [ ] auto pic change at 12h (start tracking on boot)
- [x] handle button changes script runs on boot and restarts if it crashes
- [x] pic change on button press
- [x] pic prepare script resize and rotate images
- [x] nodejs webapp for pic upload
- [x] pic change script that retains current image index

---

### ToDo

Basic features

- [ ] wifi hostpot mod and web app running on port 80 with mdns .local

Advanced features

- [ ] ability to disply text (disply text script)
- [ ] ability to see all the pictures in memory
- [ ] ability to select what picture to display from the web app
- [ ] make the GUI mobile first and verry pretty
- [ ] resize and process images on upload on the client side or even localy if its not to resource heavy (limit to 30 pics?)
- [ ] ability to connect to sentimental box and send qoutes with matching pics
- [ ] partial implementation show qoutes on it (once every 3 days)

---
## Systemctl handle buttons script

sentimental-frame-button-handler runs on starup using systemctl
1) add this script at: ``nano /etc/systemd/system/sentimental-frame-buttons.service ``

```bash

[Unit]
Description=Sentimental Frame Button Handler
After=network.target

[Service]
ExecStart=/home/serban/Projects/sentimental-frame/env/bin/python /home/serban/Projects/sentimental-frame/sentimental-frame-button-handler.py
WorkingDirectory=/home/serban/Projects/sentimental-frame
Restart=always
User=serban
Group=serban
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

```
2) Reload systemd to apply the new service file
``sudo systemctl daemon-reload``

3) Enable the service to run at startup
``sudo systemctl enable sentimental-frame-buttons.service``

4) Start the service immediately
``sudo systemctl start sentimental-frame.service``

Command to check the service:
``systemctl status sentimental-frame.service``

Command to debug the runnig script:
``journalctl -u sentimental-frame.service -f``

Command to stop the running script:
``sudo systemctl stop sentimental-frame.service``

## Systemctl next image script timer

1) Create a service file for your script:
``sudo nano /etc/systemd/system/sentimental-frame-next-image.service``

2) Add the following content to the service file:
```bash
[Unit]
Description=Run Sentimental Frame Next Image Script
After=network.target

[Service]
ExecStart=/home/serban/Projects/sentimental-frame/env/bin/python /home/serban/Projects/sentimental-frame/sentimental-frame-next-image.py
WorkingDirectory=/home/serban/Projects/sentimental-frame
User=serban
Group=serban
Environment=PYTHONUNBUFFERED=1
```

3) Create a Timer File
`` sudo nano /etc/systemd/system/sentimental-frame-next-image.timer ``

4) Add to the file:

```bash
[Unit]
Description=Run Sentimental Frame Next Image Script Every Minute

[Timer]
OnBootSec=1min
OnUnitActiveSec=1min
AccuracySec=1s

[Install]
WantedBy=timers.target

```
5) Enable and Start the Timer
```bash
sudo systemctl daemon-reload
sudo systemctl enable sentimental-frame-next-image.timer
sudo systemctl start sentimental-frame-next-image.timer
```

6) Verify the Timer
```bash
systemctl list-timers --all | grep sentimental-frame-next-image
journalctl -u sentimental-frame-next-image.service -f
```