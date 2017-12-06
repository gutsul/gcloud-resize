
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
Dec  6 12:28:58 test-resize /gcloud-resize.py: DEBUG: ACTION="Get instance name" INSTANCE="test-resize"
Dec  6 12:28:58 test-resize /gcloud-resize.py: DEBUG: ACTION="Get geo zone" ZONE="us-east1-c"
Dec  6 12:28:58 test-resize /gcloud-resize.py: DEBUG: ACTION="Run shell" COMMAND="lsblk --output name,mountpoint --pairs --bytes" OUT="NAME="sda" MOUNTPOINT=""#012NAME="sda1" MOUNTPOINT="/"#012NAME="sdb" MOUNTPOINT="/mnt/disks/disk1"#012" ERR=""
Dec  6 12:28:58 test-resize /gcloud-resize.py: DEBUG: ACTION="Checking disk" LABEL="sdb" NAME="disk-1" MOUNTPOINT="/mnt/disks/disk1" TOTAL_GB=12 USED_GB=12 FREE_GB=0.9251796875 FREE_%=7.900000000000006
Dec  6 12:28:58 test-resize /gcloud-resize.py: DEBUG: ACTION="Low disk" LABEL="sdb" NAME="disk-1" MOUNTPOINT="/mnt/disks/disk1"
Dec  6 12:28:58 test-resize /gcloud-resize.py: DEBUG: ACTION="New disk size" LABEL="sdb" NAME="disk-1" MOUNTPOINT="/mnt/disks/disk1" ADD_GB=3 NEW_SIZE_GB=15
Dec  6 12:28:59 test-resize /gcloud-resize.py: DEBUG: ACTION="wait resize" STATUS="PENDING"
Dec  6 12:29:05 test-resize /gcloud-resize.py: DEBUG: ACTION="wait resize" STATUS="DONE"
Dec  6 12:29:05 test-resize /gcloud-resize.py: DEBUG: ACTION="Run shell" COMMAND="sudo resize2fs /dev/sdb" OUT="Filesystem at /dev/sdb is mounted on /mnt/disks/disk1; on-line resizing required#012old_desc_blocks = 1, new_desc_blocks = 1#012The filesystem on /dev/sdb is now 3932160 blocks long.#012#012" ERR="resize2fs 1.42.9 (4-Feb-2014)#012"

```
