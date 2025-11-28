from pyfirmata2 import Arduino
from dotenv import load_dotenv
from os import environ  

load_dotenv()

class ArduinoController:
    def __init__(self, port=environ.get("PORT")):
        try:
            self.board = Arduino(port)
            self.board.samplingOn()
        except:
            raise ValueError("Arduino not found")
    
    def initialiseServos(self, *ServoPins):
        self.servos = []
        for pin in ServoPins:
            self.servos.append(self.board.get_pin(f"d:{pin}:s"))
    
    def moveServo(self, servoIndex, angle):
        self.servos[servoIndex].write(angle)

    def exitBoard(self):
        self.servos = []
        self.board.exit()

