# DHCP Python Implementation

### Server
By running the server it will wait for a client connection  
![Imgur](https://imgur.com/aP1hnQH.png)

### Client 1
connecting client 1  
![Imgur](https://imgur.com/TbhliB6.png)

### Client 2
connecting client 2  
![Imgur](https://imgur.com/JgHnnVx.png)

### Admin Clinet
You can then run the admin client to see what IP have been given out  
![Imgur](https://imgur.com/ntajEG7.png)

## Aditional Client Options
### The client is also able to release their IP and Renew their IP
- Releasing an IP will set ACKED to "False" and set the Timestamp to the current time, allowing new clients to take the IP if all others are taken.
- Renewing an IP will set the ACKED to "True" and renew the timestamp to 60 seconds from the current time.

## Attacker Client
I also have an attacker client included. This client will perform a DoS attack on the DHCP server by sending enough DISCOVER messages to fill up the pool of available IP's this prevents any new clients from connecting to the server until the timestamp on the IP's expires.

