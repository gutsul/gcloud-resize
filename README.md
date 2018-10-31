# GCloud resize tool v0.9.7

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


### Install dependencies

```bash
# Install python
sudo apt-get install -y python3-pip

# For XFS support
sudo apt-get -y install xfsprogs
```

### Install gcloud-resize tool

```bash
# Clone repo
git clone https://github.com/gutsul/gcloud-resize.git

# Go to repo folder
cd gcloud-resize/

# Install
sudo python3 setup.py install
```

## Configuration

General configuration file located in `/etc/gcloud-resize/gcloud-resize.conf`.
It consist from 3 general parts: `GCloud Settings`, `Resize Settings`, `Slack Settings`.


### GCloud Settings

| Key         | Value        | Type     | Description                                                                                      |
| :---------- | ------------ | :------: | ------------------------------------------------------------------------------------------------ |
| `ProjectId` | _project-id_ | Required | Google project id. More detail see [here](https://support.google.com/cloud/answer/6158840?hl=en).|

### Resize Settings

| Key            | Value | Type     | Description                                                                                      |
| :------------- | ----- | :------: | ------------------------------------------------------------------------------------------------ |
| `UsagePercent` | _95_  | Required | Resize disk when disk usage more or equal UsagePercent value.<br>The value should be greater than zero. |
| `ResizePercent`| _10_  | Required | Determines how much in percentage you should increase the disk when low disk space amount is detected. <br>The minimum disk space you can add is **1 GB**.|

### Slack Settings

| Key           | Value                     | Type     | Description                                          |
| :------------ | ------------------------- | :------: | ---------------------------------------------------- |
| `SlackWebhook`| _https://hooks.slack.com_ | Optional | Slack incoming webhook url.                          |
| `SlackUsers`  | _username1,username2_     | Optional | Users who will be notified about the resize message. |


## Crontab

To configure how often need to check disks, edit you root crontab.

```bash
# Edit root crontab:
sudo crontab -e

# Add lines below to end of file:

# Check persistent disks 
0 * * * * /usr/local/bin/gcloud-resize
```

### Calculate crontab job frequency

To calculate frequency _(f)_ use next formula:
```json
f = (T * r) / (2 * w )
```
Where:
- _T_ Total disk size in MB.
- _r_ Resize percent value. (5% = 0.05)
- _w_ Write rate in MB per minute

The result of the calculation means to run crontab job at least every _f_ minutes. 


## Logs

Log file located in `/var/log/gcloud-resize/gcloud-resize.log`

## Uninstall

To completely remove gcloud-resize tool run those commands in terminal:

```bash
sudo pip3 uninstall gcloud-resize
sudo rm /usr/local/bin/gcloud-resize
sudo rm -rf /etc/gcloud-resize/
sudo rm -rf /var/log/gcloud-resize/
```