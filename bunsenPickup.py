"""

This file is pretty much completely useless.

Don't want to delete rn incase it becomes useful in future.

"""



# # Imports
# import time
# import random
# import sys
# sys.path.append('../src') 
# from robot_controller import robot
# import paho.mqtt.client as mqtt
# import json
# import diceDetection
# import sorting
# import bunsen

# # BeakerIP = '172.29.208.124'
# BunsenIP = '172.29.208.123'

# # MQTT Parameters
# broker = "172.29.208.74"
# port = 1883
# pubTopic = "bunsen/"
# subTopic = "beaker/"

# robot_id = "bunsen"

# def genJSON(sender, reciever, action, position, iteration):
#     responseData = {
#         "sender": sender,
#         "reciever": reciever,
#         "action": action,
#         "position": position,
#         "iteration": iteration
#     }

#     return json.dumps(responseData)

# def on_connect(client, userdata, flags, rc, properties):
#     print("========================")
#     print(f"{robot_id} CONNECTED WITH RC: {str(rc)}")
#     print("========================")
#     client.subscribe(subTopic)
#     main()

# def on_message(client, userdata, msg):
#     data = json.loads(msg.payload.decode())
#     # elif (data["reciever"] == robot_id):
#     #     # Message not meant for this bot
#     #     return
#     position = bunsen.read_current_cartesian_pose()
#     otherPosition = data["position"]

#     iteration = data["iteration"]

#     if (data["action"] == "MoveToGrabDice"):
#         print("Moving to grab dice")
#         print(otherPosition)
#         print(position)
#         moveToDice(otherPosition)
#         position = bunsen.read_current_cartesian_pose()

#         response = genJSON(robot_id, "bunsen", "BackOff", position, iteration)
#         client.publish(pubTopic, response)
#     elif (data["action"] == "MoveToRandPos"):
#         print("Move to a random position")
#         moveToRandPos()
#         position = bunsen.read_current_cartesian_pose()
#         response = genJSON(robot_id, "bunsen", "MoveToGrabDice", position, iteration)
#         client.publish(pubTopic, response)
#     elif (data["action"] == "ConfirmAtHome"):
#         print("Confirm at home")
#         # goToBackoff()
#         position = bunsen.read_current_cartesian_pose()
#         print(position)
#         MoreToCome(position)
#         response = genJSON(robot_id, "bunsen", "StartProgram", position, iteration)
#         client.publish(pubTopic, response)
#     elif (data["action"] == "GoToHome"):
#         print("\nGoing to home\n")
#         goToHome()
#         time.sleep(1)
#         response = genJSON(robot_id, "bunsen", "GoToHome", position, iteration)
#         client.publish(pubTopic, response)
#     elif (data["action"] == "BackOff"):
#         bunsen.schunk_gripper("open")
#         time.sleep(0.5)
#         # goToBackoff()
#         position = bunsen.read_current_cartesian_pose()
#         print(position)
#         MoreToCome(position)
#         position = bunsen.read_current_cartesian_pose()
#         response = genJSON(robot_id, "bunsen", "MoveToRandPos", position, iteration)
#         client.publish(pubTopic, response)
#     elif (data["action"] == "END"):
#         global keepRunning
#         keepRunning = False
#         goToHome()
#         return

# def main():
#     random.seed()
#     global bunsen
#     global iteration 
#     iteration = 0

#     # beaker = robot(BeakerIP)
#     bunsen = robot(BunsenIP)
#     # beaker.set_speed(300)
#     bunsen.set_speed(300)

#     print("========================")
#     print("START OF PROGRAM")
#     print("========================")

# def goToHome():
#     # Both go kgp
#     bunsen.schunk_gripper("open")
#     # bunsen.schunk_gripper("open")
#     bunsen.write_joint_pose(bunsen_home)
#     # bunsen.write_joint_pose(bunsen_home)

# """
# def pickUpDice():
#     beaker.write_cartesian_position(k_diceprep)
#     beaker.write_cartesian_position(k_dicepos)
#     beaker.schunk_gripper("close")
#     time.sleep(0.5)
#     beaker.write_cartesian_position(k_diceprep)
# """
    
# def goToBackoff():
#     # currentPosition = bunsen.read_current_cartesian_pose()
#     # currentPosition[1] += 50
#     # print(currentPosition)
#     # bunsen.write_cartesian_position(currentPosition)
#     bunsen.write_joint_pose(n_backoff_okay)
#     # beaker.write_joint_pose(k_backoff)

#     #K wait & listen for ready
#     # k_random = [v + 300 * random.random() for v in k_origin] + k_orient
#     # beaker.write_cartesian_position(k_random)
#     #K transmit new postion

# def moveToDice(k_random):

#     n_trans = [a + b for a,b in zip(k_random[0:3], k_n_offset)] + n_orient
#     bunsen.write_cartesian_position([n_trans[0], n_trans[1]+50] + n_trans[2:6])
#     bunsen.write_cartesian_position(n_trans)
#     bunsen.schunk_gripper("close")
#     # N transmit grabbed

#     time.sleep(0.5)
#     # beaker.schunk_gripper("open")
#     # beaker.write_cartesian_position([k_random[0], k_random[1]-50] + k_random[2:6])
#     # beaker.write_joint_pose(k_backoff)
#     #K transmit ready

# def moveToRandPos():
#     #----Bunsen's turn to direct----
#     n_random = [v + 300 * random.random() for v in n_origin] + n_orient
#     bunsen.write_cartesian_position(n_random)
#     # N tansmit new position

#     # k_trans = [a - b for a,b in zip(n_random[0:3], k_n_offset)] + k_orient
#     # beaker.write_cartesian_position([k_trans[0], k_trans[1]-50] + k_trans[2:6])
#     # beaker.write_cartesian_position(k_trans)
#     # beaker.schunk_gripper("close")
#     #K transmit grabbed

# def MoreToCome(n_random):
#     time.sleep(0.5)
#     bunsen.schunk_gripper("open")
#     n_random[3] += 1
#     bunsen.write_cartesian_position([n_random[0], n_random[1]+50] + n_random[2:6])
#     bunsen.write_joint_pose(n_backoff_okay)
#     #N Transmit Ready
#     # End of loop

#     # beaker.write_cartesian_position(k_diceprep)
#     # beaker.write_cartesian_position(k_dicepos)
#     # beaker.schunk_gripper("open")

#     # beaker.write_cartesian_position(k_diceprep)

#     # beaker.write_joint_pose(beaker_home)
#     # bunsen.write_joint_pose(bunsen_home)

#     print("==============================")
#     print("END OF PROGRAM")
#     print("==============================")

# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# client.on_connect = on_connect
# client.on_message = on_message

# client.connect(broker, port)

# client.loop_start()

# keepRunning = True


# while keepRunning:
#     time.sleep(1)

# client.loop_stop()
# client.disconnect()