import numpy as np

class ScenarioParameters:
    def __init__(self):
        # Default parameters (initial values)
        self.frequency = None
        self.phase = None
        self.curvature_angle = None
        self.position_between_transmitters = None
        self.num_transmitters = 2
        self.array_geometry = None

    def set_5g_parameters(self):
        self.frequency = 1000000000  # Frequency in MHz
        self.phase = 0 
        self.curvature_angle = 30  # Degrees
        self.position_between_transmitters = 100000  # Distance in micrometers
        self.num_transmitters = 16  # Example for massive MIMO
        self.array_geometry = "linear"

    def set_radar_parameters(self):
        self.frequency = 1600000000  # Frequency in kHz
        self.phase = 90
        self.curvature_angle = 30  # Degrees
        self.position_between_transmitters = 3000  # Distance in micrometers
        self.num_transmitters = 32 # Example for ultrasound transducers
        self.array_geometry = "linear"

    def set_tumor_ablation_parameters(self):
        self.frequency = 2000000000  # Frequency in kHz
        self.phase = 0 
        self.curvature_angle = 60  # Degrees
        self.position_between_transmitters = 50000  # Distance in micrometers
        self.num_transmitters = 4  # Example for tumor ablation
        self.array_geometry = "curved"

    def reset_parameters(self):
        self.frequency = 1000000000
        self.phase = 0
        self.curvature_angle = 30
        self.position_between_transmitters = 0
        self.num_transmitters = 2  
        self.array_geometry = "curved" 
       



    def update_parameters(self, scenario):
        """
        Updates the parameters based on the selected scenario.
        :param scenario: A string ('5G', 'Airborne Radar', 'Tumor Ablation')
        """
        if scenario == "5G":
            self.set_5g_parameters()
        elif scenario == "Airborne Radar":
            self.set_radar_parameters()
        elif scenario == "Tumor Ablation":
            self.set_tumor_ablation_parameters()
        else:
            self.reset_parameters()

    def display_parameters(self):
        """Displays the current parameters in a readable format."""
        print(f"Frequency: {self.frequency}")
        print(f"Phase: {self.phase}")
        print(f"Curvature Angle: {self.curvature_angle}")
        print(f"Number of Transmitters: {self.num_transmitters}")

