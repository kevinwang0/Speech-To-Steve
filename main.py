from speech import record_audio
from Command import Command
from Process import Process
#from basic_movement import BasicMovement
from malmo_commands import SpeechToSteve
from speech_recognition import UnknownValueError
from speech_recognition import RequestError
import time

if __name__ == "__main__":
    process = Process(SpeechToSteve({}))
    while True:
        try:
            i = input("Ready for command")
            command =  record_audio() 
            #command = str(input("Type your command: ")) #keyboard input
            command = Command(command)

            print("raw_text", command.rawText)
            for token in command.doc:
                print(token.text, end=' ')
                print(token.dep_, token.pos_)    
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        except UnknownValueError:
            print("Cannot recognize audio")
            continue
        except RequestError:
            print("Speech service down")
            print("Exiting")
            break

        if "exit" in command.rawText:
            print("Exiting")
            break
        
        #print(command.parse())
        process.process_command(command)
