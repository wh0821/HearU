# HearU
![HearU](https://github.com/Boheng2/HearU/blob/main/HearU-logo.png)

## Inspiration
Speech is one of the fundamental ways for us to communicate with each other, but many are left out of this channel of communication. Around half a billion people around the world suffer from hearing loss, this is something we wanted to address and help remedy.  

Without the ability to hear, many are locked out of professional opportunities to advance their careers especially for jobs requiring leadership and teamwork.  Even worse, many have trouble creating fulfilling relationships with others due to this communication hurdle. 

Our aim is to make this an issue of the past and allow those living with hearing loss to be able to do everything they wish to do easily. 
HearU is the first step in achieving this dream.
![Speech is one of the fundamental ways for us to communicate with each other, but many are left out of this channel of communication. Around half a billion people around the world suffer from hearing loss, this is something we wanted to address and help remedy.  

Without the ability to hear, many are locked out of professional opportunities to advance their careers especially for jobs requiring leadership and teamwork.  Even worse, many have trouble creating fulfilling relationships with others due to this communication hurdle. 

Our aim is to make this an issue of the past and allow those living with hearing loss to be able to do everything they wish to do easily. 
HearU is the first step in achieving this dream.
](https://github.com/Boheng2/HearU/blob/main/HearUWhyItMatters.png)

## What it does

HearU is an inexpensive and easy-to-use device designed to help those with hearing loss understand the world around them by giving them subtitles for the world. 
The device attaches directly to the user’s arm and automatically transcribes any speech heard by it to the user onto the attached screen. The device then adds the transcription on a new line to make sure it is distinct for the user. 
A vibration motor is also added to alert the user when a new message is added. The device also has a built in hazard detection to determine if there are hazards in the area such as fire alarms. HearU also allows the user to store conversations that took place locally on the device for privacy.  
Most Importantly, HearU allows the user to interact without with ease with others around them.











## How we built it
HearU is based on a Raspberry Pi 4, and uses a display, microphone and a servo motor to operate and interface with the user. A Python script analyzes the data from the microphone, and updates the google cloud API, recording the real-time speech and then displaying the information on the attached screen. The frontend is then rendered with a python library called pyQT. The entire device is enclosed in a custom built 3d printed housing unit that is attached to the user’s arm.
This project required a large amount of different parts that were not standard as we were trying to minimize size as much as possible but ended up integrating beautifully together.


## Challenges we ran into

The biggest challenge that we ran into was hardware availability. I needed to scavenge for parts between multiple different sites, which made connecting “interesting” to say the least since we had to use 4 HDMI connectors to get the right angles we needed. Finding a screen that was affordable, that would arrive on time and the right size for the project was not easy.  

Trying to fit all the components into something that would fit on an arm was extremely difficult as well and we had to compromise in certain areas such as having the power supply in the pocket for weight and size constraints. We started using a raspberry pi zero w at first but found it was too underpowered for what we wanted to do so we had to switch to the pi4. This meant we had to redesign the enclosure.

We were not able to get adequate time to build the extra features we wanted such as automatic translation since we were waiting on the delivery of the parts, as well as spending a lot of time troubleshooting the pi. We even had the power cut out for one of our developers who had all the frontend code locally saved! 

In the end we are happy with what we were able to create in the time frame given.

## Accomplishments that we're proud of
I’m proud of getting the whole hack to work at all! Like I mentioned above, the hardware was an issue to get integrated and we were under a major time crunch. Plus working with a team remotely for a hardware project was difficult and our goal was very ambitious. 
We are very proud that we were able to achieve it!


## What we learned

We learned how to create dense electronic devices that manage space effectively and we now have a better understanding of the iterative engineering design process as we went through three iterations of the project. We also learned how to use google cloud as it was the first time for any of us have used it. Furthermore we learned how to create a good looking UI using just python and pyqt. Lastly we learned how to manipulate audio and various audio fingerprinting algorithms to match audio to sounds in the environment.


## What's next for HearU


There are many things that we can do to improve HearU.

We would like to unlock the potential for even more communication by adding automatic language translation to break down all borders. 

We can also miniaturize the hardware immensely by using more custom built electronics, to allow HearU to be as cumbersome and as easy to use as possible.



We would work on Integrating a camera to track users’ hands so that we can convert sign language into speech, so that those with hearing impairments can easily communicate with others, even if they don’t know sign language.





Elevator pitch

HearU is a device that gives subtitles to the world. It allows those with hearing disabilities to break through all communication hurdles they face and be able to achieve more with ease. 
