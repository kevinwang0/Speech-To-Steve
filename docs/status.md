---
layout: default
title:  Status
---
## Video Summary

[![Speech-To-Steve](https://img.youtube.com/vi/an3ZCRidCkI/0.jpg)](https://www.youtube.com/watch?v=an3ZCRidCkI)

## Summary of the Project
The main idea of our project is using Python to implement a way for the user to control the AI agent via speech. We used natural language processing to convert audio into commands, and let the agent perform all of them in Minecraft. For example, saying “kill the cow, find a goat and then move backwards for 6 steps” into a microphone would create 3 commands: "kill cow", "find goat", and "move backwards(6)", which automatically call the responding functions and let the agent to execute these commands. To accomplish this, we first converted speech to text using SpeechRecognition, and then converted the text into commands using spaCy, a library for advanced NLP, so that the agent can perform using Malmo. 

## Approach
We plan to use supervised machine learning algorithms for natural language processing and text analysis, such as SVM and Neural Networks, with the support of the SpeechRecognition Library. We will also use the PyAudio library to parse microphone input into audio data that can be sent to a speech recognition API. Specifically, we are planning on using the Google Cloud Speech API to parse the audio data of user-given commands, which would then be further analyzed with the spaCy library. The agent would then execute the required tasks by calling a certain function related to the command using the Malmo platform. 
### Part 1: Speech Recognition
We used Pyaudio to record the user's audio, and then parsed the audio input using Google Cloud Speech API in SpeechRecognition to convert the voice commands into text. We set the energy threshold "duration" to 1 in order to recognize speech right after it starts listening. In this part, users' voice commands will be converted into text and stored as a string. 
### Part 2: Information Extraction and Context Understanding
We used spaCy to call a NLP object that contains all the components and data needed to process the text, and calling the NLP object returns a processed doc object that contains all of the information of the original text as tokens. 

To further process and understand our commands, we created a Command class. In the class functions, we used NeuralCoref to replace pronouns (e.g. it, my), and then iterate every token of the processed doc to extract verbs and their corresponding direct objects/numbers, and finally combine the verbs and objects to the command that can be passed to functions of Malmo we created. Specifically, verbs are extracted from the doc object by anaylyzing its part-of-speech and dependency tagging, and then store it in a list. We also created words of interest for every verb, such as its direct objects and numbers indicating how many times we need to repeat certain commands. For example, if the text of the doc object is "Go and find a sheep and cow, and then jump six times", then the verbs and their words of interest are "go", "find" with "sheep", "cow", and "jump" with "six".

To combine this information in a way that can be processed by Malmo commands, we created a dict object with extracted verbs as keys and their words of interests as values. In addition, we implemented the similarity check so that the agent could regard the similar commands as the same one. For example, commands "go forward" and "walk forward" would call the same function walk_forward().
### Part 3: Command Execution in Malmo
We have implemented continuous movement by calling built-in commands in Malmo and adjusting the sleep time in-between commands accordingly.Commands implemented as of the status report include basic movement; such as jumping, walking (in any direction), running, etc. 
## Evaluation
We will evaluate the success of our project based on the complexity of the commands we can implement accurately and how well the agent performs tasks. There are different tiers of difficulty for commands: “walk to the right” is much easier to implement than “find and mine a diamond.” We are aiming to implement commands that are pretty complex and interact with the environment (e.g. “place down a dirt block to the left,” “take a gold ingot from the chest”), with a moonshot case being extremely complex commands that need contextual understanding (e.g. “enter the third house on the right”).

### Quantitative:
We intend to evaluate our success quantitatively by measuring the accuracy of our voice commands. In other words, we will calculate the proportion of successfully recognized voice commands to the total number of voice commands given. We will also calculate the command completion rate (e.g. the agent actually moves north when given the command to go north, the agent can recognize objects in Minecraft successfully).
 
### Qualitative:
We intend to evaluate our success qualitatively by visually checking if the agent can actually perform commands. For example, we will check if the agent actually moves 5 blocks to the left if it is given the command “walk 5 blocks left.”


| Single Command  | Multiple | Synonym | 
| -------------   | ------------- |  ------------- |
|walk to the left for 10 steps  | walk 10 steps, then run 10 steps to the right, and then jump 5 times |hurdle 5 times go forward for 10 blocks |
| Voice Recognized | Voice Recognized  | Voice Recognized |
| Command Excecuted Successfully | Command Excecuted Successfully   | Command Excecuted Successfully  |
  
## Remaining Goals and Challenges
- Information Extraction and Filtering
  Since this project is about voice recognition, the commands that our users give might have a lot of words that are semantically meaningless to the content of the commands. Take a basic statement for an example: "go" is useless in the sentence "go and find a cow", so we need to filter such words. Although we are able to filter many of these words and extract the most useful ones, we still need to improve the accuracy so that our agent can execute every commands given with desirable performance.  

- Understand More Complex Commands
  At this stage, our agent is able to recognize single, multiple and synonymous commands. We have not yet finished implementing more advanced commands, such as "kill the cow," so this part needs to be further tested. 

- Similarity Check
  In addition, we are encountering the problem that our agent may regard "run" and "walk" as the same command if we activate our similarity check. It's hard to define similarity between words; for example, the statements "I like pizza" and "I like flowers" both talk about one's preferences, but are dissimiliar in regards to their categorization. 

- Advanced Commands in Malmo
  After achieving the basic voice commands recognition and execution in malmo, we will work on letting agent execute more advanced commands like finding objects and performing actions on them. 
## Resources Used
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)\
library for performing speech recognition
- [PyAudio](https://pypi.org/project/PyAudio/)\
record audio input from microphone
- [spaCy](https://spacy.io/usage/spacy-10z)\
information extraction and natural language understanding
- [NeuralCoref](https://github.com/huggingface/neuralcoref/pulls)\
a pipeline extension for spaCy 2.1+ which annotates and resolves coreference clusters using a neural network



