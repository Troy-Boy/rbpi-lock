# rpbi-lock

Python script for verifying and unlocking Navigo boats lock

# Setup on computer

1. Install Python (running on `Python 3.10.11`)
2. Create virtual environment
    * `python -m venv <env_name>`
3. Activate the virtual environment
    * `path/to/env/Scripts/activate`
4. Install dependencies and libraries
    * `pip install -r requirements.txt`
5. Call `main.py` to start the script
    * `python main.py`
6. Once done, deactivate the virtual environment, to return to global Python environment
    * `<env_name>\Scripts\deactivate`

# Setup RaspberryPi

1. Download your wanted rbpi OS image on a SD card
2. Configure the necessary stuff (wifi, hostname, username/password, etc)
> I used this [guide](https://docs.sunfounder.com/projects/raphael-kit/en/latest/install_setup_os/installing_the_os.html) for my setup
3. For ssh:
    1. Run powershell as administrator on your computer
    2. Ping the the rbpi's IP with `ping -4 <hostname>.local`
    	> Usually, the hostname is set to `raspberrypi`
    3. If your rbpi is connected to the same network as your computer, you will see the IP address
    4. Once the IP address is confirmed, log in to your Raspberry Pi using `ssh <username>@<hostname>.local` or `ssh <username>@<IP address>`

4. For deskstop: 
    
    If you installed the OS desktop version on the rbpi, you can connect an HDMI-to-miniHDMI cable to a screen and your rpbi. You can use it same as a computer, just connect a keyboard and mouse.

5. Enable i2c https://docs.sunfounder.com/projects/raphael-kit/en/latest/appendix/i2c_configuration.html#i2c-config


6. Enable SPI coonfiguration https://docs.sunfounder.com/projects/raphael-kit/en/latest/appendix/spi_configuration.html

7. Install Spidev and MFRC522 https://docs.sunfounder.com/projects/raphael-kit/en/latest/appendix/install_the_libraries.html#spidev-and-mfrc522

6. Download the repo (private for now)

7. Enable run on boot for the script #TODO: that


# Setup SixFab base hat

1. Install the hat and all it's components on the raspberryPi: https://docs.sixfab.com/docs/raspberry-pi-4g-lte-cellular-modem-kit-getting-started

2. To set up the SixFab software, follow this guide: https://www.twilio.com/docs/iot/supersim/getting-started-super-sim-raspberry-pi-sixfab-base-hat#3-connect-to-the-internet

> Important:
> You need to create a SixFab account and activate the relevant SIM card with the ICCID number on the SIM.
> For testing purposes, use the `atcom AT+<command>` to troubleshoot the SIM status: https://docs.sixfab.com/docs/raspberry-pi-3g-4g-lte-base-hat-troubleshooting



# Troubleshooting
Here are the most common errors encountered in the project:

1. The LCD screen use either address 0x27 or 0x3f. If, by unknown reason, it uses another one, change the script in LCD1602.py at `init(addr=None, bl=1)` for:

```python
def init(addr=None, bl=1):
	global LCD_ADDR
	global BLEN

	i2c_list = i2c_scan()
	print(f"i2c_list: {i2c_list}")
	if addr is None:
		if '27' in i2c_list: 
			LCD_ADDR = 0x27
		elif '3f' in i2c_list:
			LCD_ADDR = 0x3f
        elif 'the-new-lcd-address':
            LCD_ADDR = 0x+"the-new-lcd-address"
		else:
			# raise IOError("I2C address 0x27 or 0x3f no found.")
			LCD_ADDR = 0x3f
```

2. SixFab base hat is not as intuitive as one would expect. You might need to change internet connection priority to be on the SIM card first, WIFI second.

3. Make sure the SixFab connects to the LTE on boot.