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