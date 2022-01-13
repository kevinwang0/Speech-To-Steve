---
layout: default
title: Proposal
---
# Summary of the Project
The main idea of our project is to use Python to implement a way for the user to control the AI agent via speech. We plan on using natural language processing to convert audio into commands for the agent to perform in Minecraft. For example, saying “kill the cow” into a microphone would lead to the agent killing a cow in the Minecraft mission. To accomplish this, we intend on converting speech to text, and then converting the text into commands that the agent can perform using Malmo.

# AI/ML Algorithms
We plan to use supervised machine learning algorithms for natural language processing and text analysis, such as SVM and Neural Networks, with the support of the SpeechRecognition Library. We will also use the PyAudio library to parse microphone input into audio data that can be sent to a speech recognition API. Specifically, we are planning on using the Google Cloud Speech API to parse the audio data of user-given commands, which would then be further analyzed with the NLTK library. The agent would then execute the required tasks by calling a certain function related to the command using the Malmo platform. 

# Evaluation Plan

We will evaluate the success of our project based on the complexity of the commands we can implement accurately and how well the agent performs tasks. There are different tiers of difficulty for commands: “walk to the right” is much easier to implement than “find and mine a diamond.” We are aiming to implement commands that are pretty complex and interact with the environment (e.g. “place down a dirt block to the left,” “take a gold ingot from the chest”), with a moonshot case being extremely complex commands that need contextual understanding (e.g. “enter the third house on the right”).
  
### Quantitative:
We intend to evaluate our success quantitatively by measuring the accuracy of our voice commands. In other words, we will calculate the proportion of successfully recognized voice commands to the total number of voice commands given. We will also calculate the command completion rate (e.g. the agent actually moves north when given the command to go north, the agent can recognize objects in Minecraft successfully).
 
### Qualitative:
We intend to evaluate our success qualitatively by visually checking if the agent can actually perform commands. For example, we will check if the agent actually moves 5 blocks to the left if it is given the command “walk 5 blocks left.”


# Appointment with the Instructor
Appointment Date: 1/20/21 3:45 PM

# Weekly Group Meeting Time
Tuesdays 3:00 PM

