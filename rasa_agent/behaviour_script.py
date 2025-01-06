from qibullet import SimulationManager, PepperVirtual
from time import sleep
import numpy as np

# Initialize Pepper and simulation environment
def initialize_pepper():
    sim_manager = SimulationManager()
    client = sim_manager.launchSimulation(gui=True)
    pepper = sim_manager.spawnPepper(client, spawn_ground_plane=True)
    pepper.goToPosture("Stand", 0.6)
    return sim_manager, client, pepper

    
# Generate multi-modal greeting
def greet_user(pepper, user_name=None):
    if user_name:
        message = f"Hello, {user_name}! I am your career advisor. How can I help you?"
    else:
        message = "Hello! I am your career advisor. How can I help you?"

    print(message)
    make_pepper_wave(pepper)
    
    
def make_pepper_wave(pepper):
    # Define the joint names for Pepper's arm
    arm_joints = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll']
    
    # Define a simple wave motion by controlling the shoulder and elbow joints
    # You can adjust these angles to fine-tune the waving motion.
    wave_positions = [
        [1.5, 0.1, -1.0, -0.4], # Start: arm up, open palm position
        [-1.0, 1.0, -1.0, -0.8],
        [-1.0, 1.0, -1.0, 0.8],
        [-1.0, 1.0, -1.0, -0.8],
        [1.5, 0.1, -1.0, -0.4]
    ]
    
    # Make the arm move in a wave motion
    for position in wave_positions:
        pepper.setAngles(arm_joints, position, 1.0)  # Set angles for arm joints
        sleep(0.2)  # Wait for the movement to complete
    


# Goodbye function
def say_goodbye(pepper):
    print("Thank you for visiting! Goodbye and good luck with your career.")
    make_pepper_wave(pepper)

# Main execution
def main():
    sim_manager, client, pepper = initialize_pepper()
    # camera_handle = pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP)
    try:
        # bayesian_model = create_bayesian_network()
        # detect_face(camera_handle)
        greet_user(pepper)
        say_goodbye(pepper)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sim_manager.stopSimulation(client)

if __name__ == "__main__":
    main()
