# Imports
import time
import random
import sys
sys.path.append('../src') 
from robot_controller import robot
import paho.mqtt.client as mqtt
import json
import diceDetection
import sorting
from genJSON import genJSON

BeakerIP = '172.29.208.124'

robot = robot(BeakerIP)
robot.set_speed(300)
SCHUNK_SLEEP_TIME = 2.0
beaker_home = [0, 0, 0, 0,-90, 0]
beaker_dice_pos_ready_catesian = [468, -230, 153, 178, 0,0]
beaker_dice_pos_start_cartesian = [691, 193, -185, 178, 0, 32] 
diceIteration = 0

beakerCoords = []

"""
# MQTT Parameters
broker = "172.29.208.74"
port = 1883
pubTopic = "bunsen/"
subTopic = "beaker/"

robot_id = "bunsen"

k_n_offset=[  7,-2240, -15]
beaker_y_offset = 400

diceIterator = 0
def on_connect(client, userdata, flags, rc, properties):
    global beakerCoords
    print("========================")
    print(f"{robot_id} CONNECTED WITH RC: {str(rc)}")
    print("========================")
    client.subscribe(subTopic)

    # take a picture of the board, then instruct beaker to take a picture as well
    beakerCoords = takePicture()
    response = genJSON("TakePicture", [0,0,0,0,0,0])
    client.publish(response)

# Handles control flow for when robot recieves a message
def on_message(client, userdata, msg):
    global beakerCoords
    data = json.loads(msg.payload.decode())

    type = data["type"]

    if (type == "TakePicture"):
        beakerCoords = takePicture()
    elif (type == "Moving"):
        # Beaker is moving to 1) a dice or 2) home position, we need to find where it is going and calculate an offset based on that
        # to determine which dice we can pick up

        # Get the position that beaker is going to be at
        position = data["dicePosition"]

        # Convert beaker to bunsen coordinates + y offset padding
        position[0] += k_n_offset[0]
        position[1] += k_n_offset[1] + beaker_y_offset
        position[2] += k_n_offset[2]

        # Find a dice that is within reach plus the offset
        nextDice = getValidDicePos(position)

        if (nextDice == None):
            # There are no dice beaker can pick up, wait for next signal. 
            # POTENTIAL ERROR: If beaker never sends another signal, we won't be able to re run and
            # get all the dice we need. Might need beaker to send a confirmation signal it is home. 
            # Ask Nathan for ideas.
            # If we just send "Moving" every time we go to a new location, then it should work as we will just re-roll. So, send the moving signal
            # every time we move to a dice and move back to home works I believe.
            print("No dice available for Bunsen to pick up")
            print("Bunsen will not do anything on this pass")
            print("Bunsen should return to home position, and send beaker it is returning home")
            # POTENTIAL ERROR: What happens if we get a moving at the same time? We should put the next dice to grab in a queue? But this could have some
            # errors on going to pick up the next dice? I am not sure though 
        else:
            if (robot.is_moving()):
                print("We are (potentially) already moving to a dice. Possibly store this position in a queue to go to after picking up current dice")
            else:
                # Go pick up this valid dice
                goToCoordinate(nextDice)

        # TODO Send beaker where bunsen is going now

        # Tell beaker where it is going to pick up the next dice
        response = genJSON("PickingUpDice", beakerCoords[0][diceIterator])
        diceIterator += 1
        client.publish()


def getValidDicePos(beakerPosition: list):
    # Position to compare against
    position_y = beakerPosition[1] 

    # Find entries with a y value less than position_y
    # filtered_points = [point for point in bunsenCoords[0] if point[1] < position_y]

    # Display the results
    # print("Points with y value less than", position_y, ":", filtered_points)

    # Find entries with a y value less than position_y
    first_position = next((point for point in beakerPosition if point[1] < position_y), None)
    print("First match with y value less than", position_y, ":", first_position)

    return first_position
"""

# Take a picuture, sleeping before and after to avoid race conditions
def takePicture() -> list:
    time.sleep(2)
    tmpCoords = sorting.getBeakerCoords()
    time.sleep(2)
    return tmpCoords

# go to home position
def goToHome():
    openGripper()
    robot.write_joint_pose(beaker_home)

# place dice neatly on table
def placeDice():
    robot.write_cartesian_position(beaker_dice_pos_ready_catesian)
    robot.write_cartesian_position(beaker_dice_pos_start_cartesian)
    # print(beaker_dice_pos_start_cartesian)
    openGripper()
    beaker_dice_pos_start_cartesian[2] += 70
    robot.write_cartesian_position(beaker_dice_pos_start_cartesian)
    beaker_dice_pos_start_cartesian[2] -= 70
    global diceIteration 
    diceIteration += 1

    if ((diceIteration % 3) == 0):
        beaker_dice_pos_start_cartesian[0] -= 160 
        beaker_dice_pos_start_cartesian[1] += (160*2)
    else:
        beaker_dice_pos_start_cartesian[1] -= 160
    # print(beaker_dice_pos_start_cartesian)
    robot.write_cartesian_position(beaker_dice_pos_ready_catesian)

# go to coordinate to pick up a dice
def goToCoordinate(cartesianCoordinate):
    openGripper()

    posAboveDice = cartesianCoordinate
    posAboveDice[2] += 70
    
    # Go to position of dice, just slightly above
    robot.write_cartesian_position(posAboveDice, blocking=True)

    posAboveDice[2] -= 70
    robot.write_cartesian_position(posAboveDice, blocking=True)
    posAboveDice[2] += 150

    closeGripper()

    robot.write_cartesian_position(posAboveDice, blocking=True)

    placeDice()

# open the gripper and apply a sleep timer
def openGripper():
    robot.schunk_gripper("open")
    time.sleep(1.0)

# open the gripper and apply a sleep timer
def closeGripper():
    robot.schunk_gripper("close")
    time.sleep(1.0)

def main():
    goToHome()

    # get beakers coordinates in sorted order
    beakerCoords = sorting.getBeakerCoords()

    # go to each dice and pick em up
    for coord in beakerCoords:
        goToCoordinate(coord)

    goToHome()


if __name__ == '__main__':
    main()