# GCloud resize tool v0.7

`gcloud-resize` is tool that can automatically resize persistent disks on **Google Cloud Platform**.

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
# XFS support
sudo apt-get -y install xfsprogs
```

###  Gcloud-resize tool

* Make sure you use `arbigo-prod` or `arbigo-dev` private ssh keys for **root** user.

```bash
# Clone tool to `/usr/src/gcloud-resize` folder
sudo git clone git@git.adlithium.com:arbigo/gcloud-resize.git /usr/src/gcloud-resize

# Go to gcloud-resize folder 
cd /usr/src/gcloud-resize

# Install dependencies
sudo pip3 install -r requirements.txt
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
Location `/usr/src/gcloud-resize/settings.py`

| Key                  | Type    | Value Example                          | Description |
| :------------------- | :-----: | -------------------------------------- | ----------- |
| `PROJECT_ID`         | String  | 'MyProject27'                          | **Required**. Google project id. More detail see [here](https://support.google.com/cloud/answer/6158840?hl=en).|
| `FREE_LIMIT_PERCENT` | Integer | 1 ... 99                               | **Required**. Indicates available disc space threshold at which disc space will be automatically increased.<br>The value should be greater than zero. |
| `RESIZE_PERCENT`     | Integer | 2 ... 100                              | **Required**. Determines how much in percentage you should increase the disk when low disk space amount is detected. <br> The value should be greater than `FREE_LINIT_PERCENT`.<br>The minimum disk space you can add is **1 GB**.|
| `SLACK_URL`          | String  | 'https://hooks.slack.com/'             | **Required**. Slack incoming webhook url.  |
| `SLACK_USERS`        | String  | '<@ygrigortsevich> <@victordementiev>' | **Required**. Users who will be notified about the resize message.   |


## Debug logs
See `/var/log/syslog`
```bash
Dec 18 16:24:53 localhost /gcloud-resize.py: DEBUG ACTION="Init disk." NAME="disk-1" SOURCE="/dev/sdb" FSTYPE="ext4" SIZE_GB=10 USED_GB=1 USED_%=1 AVAIL_GB=10 TARGET=/mnt/disk/disk1
Dec 18 16:24:53 localhost /gcloud-resize.py: DEBUG ACTION="Init disk." NAME="disk-2" SOURCE="/dev/sdc" FSTYPE="xfs" SIZE_GB=10 USED_GB=1 USED_%=1 AVAIL_GB=10 TARGET=/mnt/disk/disk2
Dec  7 10:57:52 test-resize /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="PENDING"
Dec  7 10:57:53 test-resize /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="RUNNING"
Dec  7 10:57:58 test-resize /gcloud-resize.py: DEBUG ACTION="wait resize" STATUS="DONE"
Dec  7 10:57:59 test-resize /gcloud-resize.py: DEBUG ACTION="J.A.R.V.I.S Say" CODE=200 STATUS="ok"
```