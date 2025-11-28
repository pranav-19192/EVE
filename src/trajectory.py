from numpy import linspace
from math import pi, cos, sin
from kinematics import inverseKinematics
from dotenv import load_dotenv
from os import environ

load_dotenv()


class trajectory:
    def __init__(self, steps):
        self.steps = steps
        self.ik = inverseKinematics(int(environ.get('L1')), int(environ.get('L2')))
        self.trajectories = {}
        self.jointAngles = {}
    
    def _generateCircularTrajectory(self, radius):
        for point in linspace(0, pi, self.steps):
            self.trajectories[point] = (radius * cos(point), radius * sin(point))
        return self.trajectories

    def _generateJointAngles(self):
        self._generateCircularTrajectory(1)
        for point in self.trajectories:
            x = self.trajectories[point][0]
            y = self.trajectories[point][1]
            self.jointAngles[point] = self.ik.calculateJointAngles(x, y)
        return self.jointAngles


