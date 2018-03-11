# Odin Eye
**Odin Eye** is a tool for doing footprinting. This tool is an online modules subset of Odin Project shown by Elias Grande ([@3grander](https://twitter.com/3grander)) and Alejandro Ramos ([@aramosf](https://twitter.com/aramosf)) at [RootedCon 2016](https://www.rootedcon.com/archive/rooted2016) conference.

## Requirements
Before **Odin Eye** usage, you must have installed Python >= 3.5.X and the requirements:

* Python 3.5.X or later
* Pip3
  * Beautifulsoup4
  * Requests
  * Dnspython

The requirements can be installed with pip:
```
    sudo pip3 install -r requirements.txt
```

## Usage

Below, a usage example would be the next one when you type `python3 odin-eye.py <target.domain>`:
```
    python3 odin-eye.py euroatlantic.pt
```

The expected output is shown below:
```
    [!] ---- TARGET: euroatlantic.pt ---- [!] 
    
    [-]  atenadev.euroatlantic.pt
         [+]  62.28.143.108
    
    [-]  autodiscover.euroatlantic.pt
         [+]  62.28.143.97
    
    [-]  citrix.euroatlantic.pt
         [+]  62.28.143.107
    
    [-]  jupiter.euroatlantic.pt
         [+]  62.28.143.98
    
    [-]  mail.euroatlantic.pt
         [+]  62.28.158.146
         [+]  62.28.143.97
    
    [-]  mx1.euroatlantic.pt
         [+]  62.28.143.99
    
    [-]  mx2.euroatlantic.pt
         [+]  62.28.183.170
    
    [-]  pop.euroatlantic.pt
         [+]  62.28.143.97
    
    [-]  saturn.euroatlantic.pt
         [+]  62.28.143.103
    
    [-]  smtp.euroatlantic.pt
         [+]  62.28.143.97
    
    [-]  webmail.euroatlantic.pt
         [+]  62.28.158.146
    
    [-]  www.euroatlantic.pt
         [+]  195.22.19.67
```

## Bugs and Feedback
For bugs, questions and discussions please use the [Github Issues](https://github.com/eliasgranderubio/odin_eye/issues) or ping me on Twitter ([@3grander](https://twitter.com/3grander)).