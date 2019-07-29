# flask-hdmi-cec
A micro API to control your TV from a RaspberryPi

## Motivation

I wanted to control a TV (Samsung UE-40J5250) using CEC. To do so there is [libcec](https://github.com/Pulse-Eight/libcec/) which provides cec-client and through that I was able to control the TV when logged into the RaspberryPi 3B+ via SSH. But I wanted to have a nice web API and began to search for something of the shelf. 

I stumbled accross [hdmi-cec-rest](https://github.com/bah2830/hdmi-cec-rest/) which is written in go but unfortunately it doesn't work for me, it shows errors after a while and does not always return the power state of the TV.

cec-client on the other hand worked like a charm for me and I decided to build a little flask app that calls cec-client in order to control the TV.

Its most likely mor of a hacky and dirty way to do it but it seems very reliable to me.

## API calls

I just implemented the bare minimum, but its very easy to extend the API if necessary.

### Get the actual State

Request: 
 - `http://<ip>:4321`
  
Response: 
 - `{"state":{"text":"standby","value":0}}`
 - `{"state":{"text":"on","value":1}}`
 - `{"state":{"text":"in transition from on to standby","value":3}}`
 - `{"state":{"text":"in transition from standby to on","value":4}}`
 - `{"state":{"text":"unknown","value":5}}`

### Turn the TV on

Request: 
 - `http://<ip>:4321/on`
 
Response: 
 - The current state (same json as a state request would return)
 
### Turn the TV off
  
Request: 
 - `http://<ip>:4321/off`
 
Response: 
 - The current state (same json as a state request would return)

## Function

The application starts a background task that periodically calls `cec-client` to get the CEC state of the TV.
If a `on` or `off` request is received, the background task will issue a cec-client call to perform the requestet action as soon as the last one has finished. 
When the state is requestet, tha last known state is returned imedialtely, if a off request comes in before a queued on command is running, the off will overwrite the on command. The same applies  the other way round.

I'm not a 100% sure if this API is perfectly threadsafe, but in my tests so far on two live systems i wasn't able to provoke any unwanted behavior.

## Setup

```
sudo apt-get install libcec4 git
sudo pip install flask gunicorn
cd /opt
sudo git clone https://github.com/Bouni/flask-hdmi-cec
cd flask-hdmi-cec
sudo cp flask-hdmi-cec.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable flask-hdmi-cec.service
sudo systemctl start flask-hdmi-cec.service
```

## Notes

I used the latest raspbian buster image for my prouction systems and cannot say for sure ig this will work with other releases!
