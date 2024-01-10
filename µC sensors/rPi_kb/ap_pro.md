```
ls                                                                  
Adafruit_Python_DHT  a.py  s.t                                                  

d@ubuntu:~$ cat s.t                                                             

wpa_supplicant -B -c /etc/wpa_supplicant/w.c -i wlan1                           
wpa_supplicant -B -c /etc/wpa_supplicant/w.c -i wlan0                           
sleep 20                                                                        
dhclient                                                                        
sleep 10                                                                        
systemctl start tomcat           
```

and then go 4 it. first list 2 wifis:

```
ip a | grep ": w" 
```

# wlxd47bb0083bc6 and wlan1

nano ~/f.c

```
#ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=root
update_config=1
country=LV

network={
        ssid="aa"
        key_mgmt=NONE
}       

```

Then get the connection:

```
sudo wpa_supplicant -B -c ~/f.c -i wlxd47bb0083bc6 
sudo dhclient
```

For passwordless AP:
```
git clone https://github.com/oblique/create_ap 
cd create_ap
sudo systemctl enable create_ap
 sudo apt install -y wireless-tools hostapd dnsmasq
```

finally:

```
sudo create_ap wlan1 wlxd47bb0083bc6 ff
```

if anything lock-like error:
```
sudo rm /tmp/create_ap.all.lock
```
