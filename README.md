# Pantheon - Insecure Camera Parsing and Intelligence
<p align="center">
  <img src="/imgs/panth_logo.png">
</p>

## About Pantheon 
Pantheon is a GUI application that allows users to display information regarding network cameras in various countries as well as a live-feed for non-protected cameras. Pantheon allows users to execute an <strong>Insecam</strong> crawler or Pantheon's <strong>Dork Query</strong> crawling algorithm. I will attempt to not be a small-minded security researcher and actually deploy efficient searching mechanisms theoretically, and actually applicable crawling algorithms by utilizing process threading; for both searching mechanisms. 

## Installation 
1. ``git clone https://github.com/josh0xA/Pantheon.git``
2. ``cd Pantheon``
3. ``pip install -r requirements.txt``
4. ``python pantheon.py``
- Note: I will later add a GUI installer to make it fully indepenent of a CLI

### Windows
- You can just follow the steps above or download the official package <a href="https://joshschiavone.com/pantheon-software/PantheonWin32.zip">here</a>.

### Ubuntu & Debian Installation 
- First, complete steps 1, 2 and 3 listed above. <br/>
- ``chmod +x distros/ubuntu_deb.sh``
- ``./distros/ubuntu_deb.sh``

## Usage 
<p align="center">
  <img src="/imgs/pantheon_example1.PNG">
</p>

(Enter) on a selected IP:Port to establish a Pantheon webview of the camera. (Use this at your own risk) <br/>

(Left-click) on a selected IP:Port to view the geolocation of the camera. <br/>
(Right-click) on a selected IP:Port to view the HTTP data of the camera. <br/>

Adjust the map as you please to see the markers. <br/>

- Also note that this app is far from perfect and not every link that shows up is a live-feed, some are login pages (Do NOT attempt to login). <br/> 


## Ethical Notice
The developer of this program, Josh Schiavone, is not resposible for misuse of this data gathering tool. Pantheon simply provides information
that can be indexed by any modern search engine. Do not try to establish unauthorized access to live feeds that are password protected - that is illegal. Furthermore, if you do choose to use Pantheon to view a live-feed, do so at your own risk. Pantheon was developed for 
educational purposes only. For further information, please visit: https://joshschiavone.com/panth_info/panth_ethical_notice.html

## Licence
MIT License<br/>
Copyright (c) Josh Schiavone
