def send_movement_command(error_x, error_y):
    # Define the gain for proportional control
    Kp = 0.1
    
    # Calculate the control signals
    right = 1500 + error_x * Kp
    forward = 1500 - error_y * Kp

    # Ensure the commands are within safe bounds
    right = max(1000, min(2000, right))
    forward = max(1000, min(2000, forward))

    # Send the commands to the drone
    vehicle.channels.overrides = {'1': right, '2': forward}
