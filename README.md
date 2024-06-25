# Pantheon - Insecure Camera Intelligence
<p align="center">
  <img src="/imgs/panth_logo.png">
</p>

## About Pantheon 
Pantheon is a GUI application that allows users to display information regarding network cameras in various countries as well as an integrated live-feed for non-protected cameras. 

### Functionalities 
Pantheon allows users to execute an <strong>API</strong> crawler. There was original functionality without the use of any API's (like Insecam), but Google TOS kept getting in the way of the original scraping mechanism. 

## Installation 
1. ``git clone https://github.com/josh0xA/Pantheon.git``
2. ``cd Pantheon``
3. ``pip3 install -r requirements.txt``<br/>
Execution: ``python3 pantheon.py``
- Note: I will later add a GUI installer to make it fully indepenent of a CLI

### Windows
- You can just follow the steps above or download the official package <a href="https://joshschiavone.com/" target="_blank">here</a>.
- Note, the PE binary of Pantheon was put together using pyinstaller, so Windows Defender might get a bit upset. 

### Ubuntu
- First, complete steps 1, 2 and 3 listed above. <br/>
- ``chmod +x distros/ubuntu_install.sh``
- ``./distros/ubuntu_install.sh``

### Debian and Kali Linux
- First, complete steps 1, 2 and 3 listed above. <br/>
- ``chmod +x distros/debian-kali_install.sh``
- ``./distros/debian-kali_install.sh``

### MacOS
- The regular installation steps above should suffice. If not, open up an issue.
- or, you can just follow the steps above or download the official package <a href="https://joshschiavone.com/" target="_blank">here</a>.
- Move it to your applications folder after installation. 
- Please note that you are going to have to run Pantheon higher privileges to utilize the file saving. <br/>
- ``$ /Applications/Pantheon.app/Contents/MacOS/Pantheon`` - after installation.

## Usage 
<p align="center">
  <img src="/imgs/pantheon_second_example.PNG">
</p>

(Enter) on a selected IP:Port to establish a Pantheon webview of the camera. (Use this at your own risk) <br/>

(Left-click) on a selected IP:Port to view the geolocation of the camera. <br/>
(Right-click) on a selected IP:Port to view the HTTP data of the camera (Ctrl+Left-click for Mac). Users can also search for keywords in the HTTP dump.<br/>

Adjust the map as you please to see the markers. <br/>

- Also note that this app is far from perfect and not every link that shows up is a live-feed, some are login pages (Do NOT attempt to login). <br/> 


## Ethical Notice
The developer of this program, Josh Schiavone, is not resposible for misuse of this data gathering tool. Pantheon simply provides information
that can be indexed by any modern search engine. Do not try to establish unauthorized access to live feeds that are password protected - that is illegal. Furthermore, if you do choose to use Pantheon to view a live-feed, do so at your own risk. Pantheon was developed for 
educational purposes only. For further information, please visit: https://joshschiavone.com/panth_info/panth_ethical_notice.html

## License
MIT License<br/>
Copyright (c) Josh Schiavone
