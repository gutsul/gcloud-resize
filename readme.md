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

### Install Python 3
```bash
sudo apt-get install python3-pip
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

## Settings
Location `/usr/src/gcloud-resize/settings.py`

| Key                  | Type    | Value Example                          | Description |
| :------------------- | :-----: | -------------------------------------- | ----------- |
| `PROJECT_ID`         | String  | 'MyProject27'                          | Required.   |
| `FREE_LIMIT_PERCENT` | Integer | 1 ... 99                               | Required.   |
| `RESIZE_PERCENT`     | Integer | 1 ... 100                              | Required.   |
| `SLACK_URL`          | String  | 'https://hooks.slack.com/'             | Required. Slack incoming webhook url.  |
| `SLACK_USERS`        | String  | '<@ygrigortsevich> <@victordementiev>' | Required. Users who will be notified about the resize message.   |


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