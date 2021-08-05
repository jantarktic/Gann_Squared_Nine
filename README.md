# Gann_Squared_Nine
This repository contains all the files and packages needed in order to run a Gann Squared Nine indicator using CQG's WebAPI and google protobuffers. 
It also contains a simplified python script containing the Gann Squared Nine indicator as a function that takes any number as an argument.

To use this strategy in CQG, download this repository and unzip the google and proto folders in your working directory. Make sure you have a working account or demo account with CQG and have access to their WebAPI.

This repository also contains the gann_signals.csv file that includes sample inputs from various amounts of runtime.

If using a demo account add "demo" to the client.connect() method like so:
client.connect('wss://api.cqg.com:443')

The packages required and the accompanying proto documents can also be downloaded here: https://partners.cqg.com/api-resources/web-api/documentation.  
