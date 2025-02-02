# Speech Trainer

## About
This project intends to use computer visuals to help stutterers practice becoming more fluent. The latest version requires a Vernier Respiratory Belt and Insignia microphone. 

The inspiration for the interface came from CAFET (Computer-Assisted Fluency Establishment Training), a computer program for clinical treatment of stuttering that was popular in the 90's and that I used myself in the late 2000's.

This program tracks your breathing and, towards the top of your inhale, adds two bars signifying when you should "turn your voice on." This helps users practice prevoice exhalation, a method where you let out a small amount of exhale before talking in order to feel a relaxed and open vocal tract. An example of these two lines can be seen below. Features such as voice tracking, feedback metrics, and an interface will be added soon. 

![alt text](https://github.com/beauhodes/spTrainer/blob/main/prevoiceExample.jpg?raw=true)

## Versions
#### V1
Version 1 allows users to view their breathing pattern and see prevoice exhalation lines signifying when to start talking. The width and timing of these lines is configurable in the code.

#### V2 (in progress)
Version 2 will add a better interface to the program. This will include a start screen where the user can run a short breathing test and then configure options such as baseline force and maximum force (for the y axis of the plot) and width/timing of the prevoice exhalation lines (when you turn your voice on).

#### V3 (planned)
Version 3 will add voice tracking. A continuous black bar will appear at the bottom of the screen when talking, and there will be breaks in the bar whenever the microphone is not picking up a voice. Performance metrics such as average duration of breath, number of stutters, number of voice breaks (pauses on a single breath caused by a stutter), and frequency of correct prevoice exhalation will also be added in this version. 

## Using the Speech Trainer
#### Hardware
Ensure that both your Vernier Respiratory Belt and Insignia microphone are plugged in and turned on.

#### Running the Program
Run 'python3 v1.py'
