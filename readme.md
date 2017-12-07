
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
Dec  7 10:57:52 test-resize /gcloud-resize.py: DEBUG: ACTION="wait resize" STATUS="PENDING"
Dec  7 10:57:53 test-resize /gcloud-resize.py: DEBUG: ACTION="wait resize" STATUS="RUNNING"
Dec  7 10:57:54 test-resize kernel: [163906.538219] sd 0:0:2:0: [sdb] 65011712 512-byte logical blocks: (33.3 GB/31.0 GiB)
Dec  7 10:57:54 test-resize kernel: [163906.538223] sd 0:0:2:0: [sdb] 4096-byte physical blocks
Dec  7 10:57:54 test-resize kernel: [163906.538765] sdb: detected capacity change from 30064771072 to 33285996544
Dec  7 10:57:54 test-resize kernel: [163906.539890] VFS: busy inodes on changed media or resized disk sdb
Dec  7 10:57:56 test-resize /gcloud-resize.py: message repeated 3 times: [ DEBUG: ACTION="wait resize" STATUS="RUNNING"]
Dec  7 10:57:58 test-resize /gcloud-resize.py: DEBUG: ACTION="wait resize" STATUS="DONE"
Dec  7 10:57:58 test-resize kernel: [163910.236359] EXT4-fs (sdb): resizing filesystem from 7340032 to 8126464 blocks
Dec  7 10:57:58 test-resize kernel: [163910.568027] EXT4-fs (sdb): resized filesystem to 8126464
Dec  7 10:57:59 test-resize /gcloud-resize.py: DEBUG ACTION="J.A.R.V.I.S Say" CODE=200 STATUS="ok"
```
