from math import atan, acos, sin, cos, degrees, pi
import os
from dotenv import load_dotenv

load_dotenv()

class inverseKinematics:

    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
    
    def calculateJointAngles(self, x, y):
        numerator = (pow(x, 2) + pow(y, 2) - pow(self.l1, 2) - pow(self.l2, 2))
        denominator = (2 * self.l1 * self.l2)
        cos_theta2 = numerator / denominator

        if cos_theta2 > 1 or cos_theta2 < -1:
            raise ValueError(f"Point ({x}, {y}) is unreachable.")
        theta2 = pi - acos(cos_theta2)

        try:                                                                                                                                                                                                                                                                                                                     
            gamma = atan(y / x)
        except ZeroDivisionError:
            raise ValueError(f"Point ({x}, {y}) is unreachable.")
        
        beta = atan(self.l2 * sin(theta2) / (self.l1 + self.l2 * cos(theta2)))
        theta1 = gamma - beta

        return degrees(theta1), degrees(theta2)

