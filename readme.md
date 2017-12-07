
## Install dependencies

### Python 3
```bash
sudo apt-get install python3-pip
```

### Packages
```bash
sudo pip3 install -r requirements.txt
```


## Debug logs
See `/var/log/syslog`
```bash
Dec  7 10:57:51 test-resize /gcloud-resize.py: DEBUG ACTION="Analyze disk" LABEL="sdb" NAME="disk-1" MOUNTPOINT="/mnt/disks/disk1" TOTAL_GB=29 USED_GB=12 FREE_GB=18 FREE_%=60.7
Dec  7 10:57:51 test-resize /gcloud-resize.py: DEBUG ACTION="Disk Low" LABEL="sdb" NAME="disk-1" MOUNTPOINT="/mnt/disks/disk1" TOTAL_GB=29 USED_GB=12 FREE_GB=18 FREE_%=60.7
Dec  7 10:57:52 test-resize /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="PENDING"
Dec  7 10:57:53 test-resize /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="RUNNING"
Dec  7 10:57:58 test-resize /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="DONE"
Dec  7 10:57:59 test-resize /gcloud-resize.py: DEBUG ACTION="J.A.R.V.I.S Say" CODE=200 STATUS="ok"
```