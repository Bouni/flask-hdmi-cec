# flask-hdmi-cec
A micro API to control your TV from a RaspberryPi

## Motivation

I wanted to control a TV (Samsung UE-40J5250) using CEC. To do so there is [libcec](https://github.com/Pulse-Eight/libcec/) which provides cec-client and through that I was able to control the TV when logged into the RaspberryPi 3B+ via SSH. But I wanted to have a nice web API and began to search for something of the shelf. 

I stumbled accross [hdmi-cec-rest](https://github.com/bah2830/hdmi-cec-rest/) which is written in go but unfortunately it doesn't work for me, it shows errors after a while and does not always return the power state of the TV.

cec-client on the other hand worked like a charm for me and I decided to build a little flask app that calls cec-client in order to control the TV.

Its most likely mor of a hacky and dirty way to do it but it seems very reliable to me.

# API calls

I just implemented the bare minimum, but its very easy to extend the API if necessary.

Request: 
 - http://192.168.178.10:4321/state
  
Response: 
 - `{"number":0,"state":"standby"}`
 - `{"number":1,"state":"on"}`
 - `{"number":2,"state":"unknown"}`

Request: 
 - http://192.168.178.10:4321/on
Response: 
 - `{"success":true}`
  
  
Request: 
 - http://192.168.178.10:4321/off
Response: 
 - `{"success":true}`
 
 Note: The requests take about 2.7 seconds to complete but I can easly deal with that.
