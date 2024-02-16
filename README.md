# Project Watchdog

## Overview
Project watchdog is a web based platform that allows users to report road accidents and crimes in his/her county of residence.  This platform will serve as a vital tool in the collective effort to enhance community safety and security. By leveraging technology, the project seeks to empower individuals to report accidents and crimes promptly, thereby facilitating quicker response times from relevant authorities. This initiative aligns with broader goals to utilize technology for the betterment of society, bridging the gap between technological innovation and community welfare.

## User instructions
The users of the website include:
  - Law enforcement (police and traffic officers)
  - Road safety agency (NTSA)
  - Citizens (who can report road accidents or crimes)

**NOTE**
  - Citizens report accidents or crimes anonymously whether he/she has created an account or not. A citizen can choose to create an account or not.
  - Reported incidents are forwarded to and can only be viewed by the respective authorities and users. Law enforcement can view both reported accidents and crimes. Road safety agency cannot view reported crimes.
  - Users mentioned above get a real time location of all reported incidents. This is displayed on a geographical map that pin points the exact location of a map.

## Developer instructions
Installation guide to run the project remotely.
```(bash)
  $ cd Desktop
  $ git clone https://github.com/morikeli/watch-dog.git
  $ python3 -m venv .watch-dog-venv
  $ source .watch-dog-venv/bin/activate
  $ pip install -r requirements.txt
```

## Contributor expectations
Incase of a bug or you wish to make an update create a new branch using git command `git checkout -b <name of your branch>` and create a pull request. Wait for review.

Don't forget to star the repo 🌟😉
