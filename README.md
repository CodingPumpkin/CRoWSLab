
# CRoWSLab
## Motivation

This app is a project from a very long time ago. I made it as a part of CRoWSLab project at uni. This project feels junky and looking back the code looks terrible. Yet this piece of old garbage is dear to my heart and I had to chance to continue developing it I would gladly do that without a second thought. I decided to put this up here because I feel like it is a huge part of my history as a programmer (it's my first ever real GUI after all! <sup><sub>no, really, it was even used by other people like once =D</sup></sub> ) 

## Installation
If you for some unholy reason want to get this baby on your computer here is the best way I know to do so.
First of all you need to have python3. That's easy enough. Then you need to have a bunch of libs (all of them are listed in the requirements.txt). I would not recommend installing them to your system because I honestly hate to bring junk I need for this one time and that's why I suggest using venv. Get yourself a virtual environment (or venv for short). Then you can go to the folder with this project and type 
``` 
virtualenv .venv
```
Activate it by running 
```
 source .venv/bin/activate
```
Then run 
```
pip install -r requirements.txt
```
It should install everything you need  to have.
The past step: run
```
python app
```
P.S. To exit the (.venv) type 
```
deactivate
```
___
## Usage
I mean...
Okay. If you are reading this and you want to know how to use this here is the best explanation I can give.
### The project
During my time at the uni my classmate an I have made this project that would potentially allow students to do electronics laboratory works remotely. We used analog switch matrices to make a circuit board with a bunch of terminals. It had 4 terminals to connect to the measuring equipment we had and also 16 terminals for the elements to be used (see illustration.jpg for a better picture). The elements for the lab come in a form of another circuit board and so you can make a make several sets of elements for the laboratory work. Then you can connect them in any way you want via the matrices. Then you can do the whole work never touching anything but your computer to send what connections you want to make and which nodes you want to measure.
### The hardware and the MC
An Arduino was used to control the hardware part. That part was done by [my classmate](https://github.com/Sergo3682). He happened to publish it [here](https://github.com/Sergo3682/crowsSimple).
###  The application part 
CRoWSLab interface supposedly has the following functions (although it's been a while since I've tested it): 
1) transfer data to the MC;
2) allow the user to select the COM port through which the data transfer should occur
3) allow the user  to load a file containing a description of the laboratory work (which holds information about all the elements in a format compatible with the pspice description),
4) display a log in which all steps of “communication” between the program and the MC are recorded
5) display images and diagrams that the user may need in the work process,
6) check the data entered by the user for simple errors.

The algorithm goes like this:
Load a lab from a netlist file (stored in src/ntlst/ by default). Select a COM port you plan on using. Connect terminals to the nodes of the circuit by writing terminals' numbers next to the nodes' numbers. You can also connect measuring equipment by filling in the fields in the right column. Select nodes to be power nodes (ground, +5V and Vref) if needed. When all setting up is done press "SEND!" and your data will be sent to the MC you've connected to the COM port. Then our circuit board will connect your circuit for you.

You can find the same algorithm in the help menu.
