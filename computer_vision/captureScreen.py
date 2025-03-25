import pyautogui
import numpy as np
import matplotlib.pyplot as plt

def captureRegion(region):
    # Capture the specified region and convert it to numpy array
    tupled_region=(region[0],region[1],region[2],region[3])
    screenshot = pyautogui.screenshot(region=tupled_region)
    return np.array(screenshot)

def displayInputs(inputs):
    for image in inputs :
        plt.imshow(image)
        plt.show()