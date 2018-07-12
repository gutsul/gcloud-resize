# GCloud resize tool v0.8

`gcloud-resize` is tool that can automatically resize persistent disks on **Google Cloud Platform**.
<br>This tool supports the next filesystems: **ext4**, **xfs**.

## Requirements

### Compute Engine

#### Labels
Set next *labels* for VM instance.
 
| Label           | Description |
| :-------------: | --------- |
| `environment`   | Environment definition. <br> For example value can be **development**, **production**, **stage**. |


#### Cloud API access scopes
Add next permissions to **Cloud API access scopes** for VM instance. 

| Cloud API       | Permissions |
| :-------------: | :---------: |
| Compute Engine  | Read Write  |


## Installation  

`gcloud-resize` tool need installed **python 3** and run with **root** permissions.

### Install Python
```bash
sudo apt-get install python3-pip
```

### Install Dependencies
```bash
# For XFS support
sudo apt-get -y install xfsprogs
```

### Install gcloud-resize tool

```bash
gcloud-resize
sudo git clone git@github.com:gutsul/gcloud-resize.git /usr/src/gcloud-resize

# Go to gcloud-resize folder 
cd /usr/src/gcloud-resize

# Install dependencies
sudo pip3 install -r requirements.txt
```

### Configure environment

Create `.env` file from sample `.env.sample` and set [settings](#settings).

```
# Go to gcloud-resize folder 
cd /usr/src/gcloud-resize

# Copy sample
cp .env.sample .env
```

### Crontab
Configure how often need to check disks.
```bash
# Edit root crontab:
sudo crontab -e

# Add lines below to end of file:

# GCloud resize 
*/5 * * * * /usr/src/gcloud-resize/gcloud-resize.py # Check every 5 minutes
```

## Settings

Location `/usr/src/gcloud-resize/.env`

| Key                  | Type    | Value Example                          | Description |
| :------------------- | :-----: | -------------------------------------- | ----------- |
| `PROJECT_ID`         | String  | 'MyProject27'                          | **Required**. Google project id. More detail see [here](https://support.google.com/cloud/answer/6158840?hl=en).|
| `FREE_LIMIT_PERCENT` | Integer | 1 ... 99                               | **Required**. Indicates available disc space threshold at which disc space will be automatically increased.<br>The value should be greater than zero. |
| `RESIZE_PERCENT`     | Integer | 2 ... 100                              | **Required**. Determines how much in percentage you should increase the disk when low disk space amount is detected. <br> The value should be greater than `FREE_LINIT_PERCENT`.<br>The minimum disk space you can add is **1 GB**.|
| `SLACK_URL`          | String  | 'https://hooks.slack.com/'             | **Required**. Slack incoming webhook url.  |
| `SLACK_USERS`        | String  | '<@username1> <@username2>'            | **Required**. Users who will be notified about the resize message.   |


## Debug logs
See `/var/log/syslog`
```bash
Dec 19 11:14:03 localhost /gcloud-resize.py: DEBUG ACTION="Init disk." NAME="disk-1" SOURCE="/dev/sdb" FSTYPE="ext4" SIZE_GB=14 USED_GB=10 USED_%=66 AVAIL_GB=5 TARGET=/mnt/disk/disk1
Dec 19 11:14:03 localhost /gcloud-resize.py: DEBUG ACTION="Init disk." NAME="disk-2" SOURCE="/dev/sdc" FSTYPE="xfs" SIZE_GB=12 USED_GB=10 USED_%=76 AVAIL_GB=3 TARGET=/mnt/disk/disk2
Dec 19 11:15:57 localhost /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="PENDING"
Dec 19 11:15:59 localhost /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="RUNNING"
Dec 19 11:16:03 localhost /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="DONE"
Dec 19 11:16:03 localhost /gcloud-resize.py: DEBUG ACTION="GCloud resize" NAME="disk-1" NEW_SIZE=16 RESPONSE="{'user': '438031059494-compute@developer.gserviceaccount.com', 'startTime': '2017-12-19T03:15:57.980-08:00', 'id': '8572997244663712258', 'name': 'operation-1513682157531-560af974d6f79-c95f1d73-10be4206', 'status': 'DONE', 'selfLink': 'https://www.googleapis.com/compute/v1/projects/adlithium-1289/zones/us-central1-a/operations/operation-1513682157531-560af974d6f79-c95f1d73-10be4206', 'zone': 'https://www.googleapis.com/compute/v1/projects/adlithium-1289/zones/us-central1-a', 'insertTime': '2017-12-19T03:15:57.721-08:00', 'targetId': '7544387413751976286', 'progress': 100, 'endTime': '2017-12-19T03:16:02.534-08:00', 'kind': 'compute#operation', 'targetLink': 'https://www.googleapis.com/compute/v1/projects/adlithium-1289/zones/us-central1-a/disks/disk-1', 'operationType': 'resizeDisk'}"
Dec 19 11:16:03 localhost /gcloud-resize.py: DEBUG ACTION="Resize disk." NAME="disk-1" ADD_GB=2 NEW_SIZE_GB=16
Dec 19 11:16:04 localhost /gcloud-resize.py: DEBUG ACTION="Apply disk." NAME="disk-1" SOURCE="/dev/sdb" FSTYPE="ext4"
Dec 19 11:16:04 localhost /gcloud-resize.py: DEBUG ACTION="Init disk." NAME="disk-1" SOURCE="/dev/sdb" FSTYPE="ext4" SIZE_GB=16 USED_GB=10 USED_%=58 AVAIL_GB=7 TARGET=/mnt/disk/disk1
Dec 19 11:16:04 localhost /gcloud-resize.py: DEBUG ACTION="J.A.R.V.I.S Say" CODE=200 STATUS="ok"
```

## Error logs
See `/var/log/syslog`
```bash
Dec 19 11:16:04 localhost /gcloud-resize.py: ERROR ACTION="Apply disk." NAME="disk-2" SOURCE="/dev/sdc" FSTYPE="xfs" REASON="Not supported file system."
```
