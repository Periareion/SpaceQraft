
import math

def default(default_value, value):
    return default_value if value is None else value


def pulse(t, P=1, A=1, y=0, FPS=60):
    return y + A*math.sin(t/FPS*math.tau/P)