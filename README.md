# Spotify test 
This is basic Client-Server application to test the backoff strategies of UDP protocol. \
When running the script the user should provide one of the two required parameters: \
 * server - to run the script as UDP server  \
  *In case of chosing server user also should provide the interface address*
 * client - to run the script as client requesting the server
  *In case of chosing client user also should provide the host address* 
Following optional command line arguments are allowed: \
  * -p 
   *Using this argument user can provide port to the UDP. Default value is 1060* \

# Example
For server side: \
 *python .\udp_spotify_v1.py server 127.0.0.1* 
 
For client side: \
 *python .\udp_spotify_v1.py client 127.0.0.1*
