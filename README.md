## Project name
xfce-caps-indicator - CapsLock indicator fot XFCE Desktop Environment.

## Table of contents
- [Project name](#project-name)
- [Table of contents](#table-of-contents)
- [General info](#general-info)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Thanks](#thanks)

## General info
In XFCE and in my keyboard, there is no indicator for CapsLock button state (on/off). Due to problems with installation of application used by me previously (indicator-keylock; missing dependencies), I decided to make my own version - in Python3.
  
## Technologies
* Backend: Python3 (integration with xfce-notification-daemon)
* Frontend: Python3 (PyGTK)

Code was tested on following platforms:
* Debian GNU/Linux bullseye/sid (Linux 5.5.0-2-amd64)

Used libraries:
* available in requirements.txt

Additional required packages:
* libindicator3-7 (Debian)
* gir1.2-appindicator3-0.1 (Debian < 10)
* gir1.2-ayatanaappindicator3-0.1 (Debian >= 10)

## Setup

1. Clone git repo to localhost.
2. Install required packages.

## Usage

For single run just do:
```
python3 xfce-caps-indicator.py
```

For startup with system: add script to autostart (for example you can use XFCE Session and Startup tool)

After XFCE starts, in notification area you will see the icon with "A" letter and arrow up. Once you press CapsLock key, you will se a notification that buton is on or off dependent of real state.


## Thanks

As always to my girlfriend!
