# Flight Bot Drone Emulator

A fun exploration into the emulation (aka spoofing) of commercial drone broadcasts


## Setting Up Dev Environment

### Prerequisites
- [conda](https://www.anaconda.com/products/distribution)- strongly encouraged to minimize environment issues
- [make](http://www.gnu.org/software/make/) - mostly used for set up, some test automation, etc.
- [pre-commit](https://pre-commit.com/) - ensures some standardization around coding and cleans up somethings for us before commits

### Setup
Assuming that you meet the prerequisites above, you can just run `make createenv` at the root of this repo. This will set up your conda environment from the local file as well as running pip to install the module locally for testing.





## References 

Work is heavily based off of the following projects

[DJI DroneID Throwie](https://github.com/DJISDKUser/ESP8266_DJI_DroneID_Throwie)
[Metasploit Drone ID Spoof](https://github.com/DJISDKUser/metasploit-framework/tree/DJIDroneIDSpoof)
