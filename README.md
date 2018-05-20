# Slacktivity

## Overview
The slack analytics page counts people leaving channels as an activity, which makes it harder to figure out which channels have gone inactive and are candidates for archiving. This script lists all the channels in a workspace with the creator name and the last date a message was posted.

## Setup
```
pip install -r requirements.txt
```

## Running
Get an API token [here](https://api.slack.com/custom-integrations/legacy-tokens). Then run:
```
python slacktivity.py TOKEN
```
To respect the API rate limits, output is limited to one channel per second.