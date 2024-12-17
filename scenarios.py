import numpy as np

class ScenarioParameters:
    def __init__(self):
        self.frequency = None
        self.phase = None
        self.curvature_angle = None
        self.position_between_transmitters = None
        self.num_transmitters = 2
        self.array_geometry = None

    def set_5g_parameters(self):
        self.frequency = 1000000000 
        self.phase = 0 
        self.curvature_angle = 30 
        self.position_between_transmitters = 100000  
        self.num_transmitters = 16  
        self.array_geometry = "linear"

    def set_radar_parameters(self):
        self.frequency = 1600000000 
        self.phase = 90
        self.curvature_angle = 30  
        self.position_between_transmitters = 3000  
        self.num_transmitters = 32 
        self.array_geometry = "linear"

    def set_tumor_ablation_parameters(self):
        self.frequency = 2000000000 
        self.phase = 0 
        self.curvature_angle = 60  
        self.position_between_transmitters = 50000  
        self.num_transmitters = 4  
        self.array_geometry = "curved"

    def reset_parameters(self):
        self.frequency = 1000000000
        self.phase = 0
        self.curvature_angle = 30
        self.position_between_transmitters = 0
        self.num_transmitters = 2  
        self.array_geometry = "curved" 
       



    def update_parameters(self, scenario):
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

