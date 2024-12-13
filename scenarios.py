import numpy as np

class ScenarioParameters:
    def __init__(self):
        # Default parameters (initial values)
        self.frequency = None
        self.phase = None
        self.curvature_angle = None
        self.position_between_transmitters = None
        self.num_transmitters = 2

    def set_5g_parameters(self):
        self.frequency = 24000  # Frequency in MHz
        self.phase = 3  # Phase in radians (e.g., π)
        self.curvature_angle = 45  # Degrees
        self.position_between_transmitters = 100000  # Distance in micrometers
        self.num_transmitters = 32  # Example for massive MIMO

    def set_ultrasound_parameters(self):
        self.frequency = 20000  # Frequency in kHz
        self.phase = 1  # Phase in radians (e.g., π/2)
        self.curvature_angle = 30  # Degrees
        self.position_between_transmitters = 3000  # Distance in micrometers
        self.num_transmitters = 8  # Example for ultrasound transducers

    def set_tumor_ablation_parameters(self):
        self.frequency = 500  # Frequency in kHz
        self.phase = 6.28  # Phase in radians (e.g., 2π)
        self.curvature_angle = 60  # Degrees
        self.position_between_transmitters = 50000  # Distance in micrometers
        self.num_transmitters = 16  # Example for tumor ablation

    def reset_parameters(self):
        self.frequency = 0
        self.phase = 0
        self.curvature_angle = 0
        self.position_between_transmitters = 0
        self.num_transmitters = 2   


    def update_parameters(self, scenario):
        """
        Updates the parameters based on the selected scenario.
        :param scenario: A string ('5G', 'Ultrasound', 'Tumor Ablation')
        """
        if scenario == "5G":
            self.set_5g_parameters()
        elif scenario == "Ultrasound":
            self.set_ultrasound_parameters()
        elif scenario == "Tumor Ablation":
            self.set_tumor_ablation_parameters()
        else:
            self.reset_parameters()

    def display_parameters(self):
        """Displays the current parameters in a readable format."""
        print(f"Frequency: {self.frequency}")
        print(f"Phase: {self.phase}")
        print(f"Curvature Angle: {self.curvature_angle}")
        print(f"Position Between Transmitters: {self.position_between_transmitters}")
        print(f"Number of Transmitters: {self.num_transmitters}")


# Example Usage
parameters = ScenarioParameters()

# Update for 5G Scenario
parameters.update_parameters("5G")
parameters.display_parameters()

# Update for Ultrasound Scenario
parameters.update_parameters("Ultrasound")
parameters.display_parameters()

# Update for Tumor Ablation Scenario
parameters.update_parameters("Tumor Ablation")
parameters.display_parameters()
