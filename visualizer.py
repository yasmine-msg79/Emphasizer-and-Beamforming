import numpy as np
import matplotlib.pyplot as plt
class Visualizer:
    def __init__(self):
        self.frequencies = [] 
        self.phases = []  
        self.magnitudes = []  
        self.array_type = "linear"  
        self.curvature_angle = 0.0  
        self.element_spacing = 0.5  

    def set_frequencies(self, frequencies):
        self.frequencies = frequencies
        if len(self.magnitudes) < len(frequencies):
            self.magnitudes = [2] * len(frequencies) 
        print(f"self.frequencies in visualizer: {self.frequencies}")
         

    def set_phases(self, phases):
        self.phases = phases
        print(f"self.phases in visualizer: {self.phases}")


    def set_array_type(self, array_type, curvature_angle):
        self.array_type = array_type
        self.curvature_angle = curvature_angle
        print(f"self.array_type in visualizer : {self.array_type}")
        print(f"self.curvature_angle in visualizer : {self.curvature_angle}")


    def calculate_positions(self):
        num_elements = len(self.frequencies)
        if self.array_type == "linear":
            return np.linspace(-num_elements * self.element_spacing / 2,
                               num_elements * self.element_spacing / 2,
                               num_elements)
        else:
            curvature = np.radians(self.curvature_angle)
            theta = np.linspace(-curvature / 2, curvature / 2, num_elements)
            return np.sin(theta) * num_elements * self.element_spacing

    def plot_beam_pattern_polar(self, num_transmitters, element_spacing, frequency, phases):
        """
        Generate and plot a full-circle beam pattern in polar coordinates.

        Parameters:
            num_transmitters (int): Number of transmitters.
            element_spacing (float): Spacing between transmitters (in meters).
            frequency (float): Frequency of waves (in Hz).
            phases (list): Phase shifts for each transmitter (in degrees).
        """
        c = 3e8  # Speed of light in m/s
        wavelength = c / frequency
        k = 2 * np.pi / wavelength  # Wave number

        # Angular range for full-circle plot (0° to 360°)
        angles = np.linspace(0, 2 * np.pi, 360)

        # Initialize the Array Factor (AF)
        AF = np.zeros_like(angles, dtype=complex)

        # Calculate the Array Factor
        for n in range(num_transmitters):
            beta = k * element_spacing * n * np.cos(angles) + np.radians(phases[n])
            AF += np.exp(1j * beta)

        # Normalize AF and convert to dB
        AF = np.abs(AF) / num_transmitters
        AF_dB = 20 * np.log10(AF + 1e-12)

        # Create the polar plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
        ax.plot(angles, AF_dB, color="blue", linewidth=2)
        ax.set_theta_zero_location("E")  # East as 0 degrees
        ax.set_theta_direction(1)  # Anti-clockwise direction
        ax.set_ylim(np.min(AF_dB) - 5, np.max(AF_dB) + 5)  # Dynamic range
        ax.set_title(f"Beam Pattern ({num_transmitters} Elements, {frequency:.1f} Hz)", va='bottom')

        return fig

    def plot_field_map(self, num_transmitters, element_spacing, frequency, phases, curvature_angle):
        """
        Generate and plot a field map in polar coordinates.

        Parameters:
            num_transmitters (int): Number of transmitters.
            element_spacing (float): Spacing between transmitters (in meters).
            frequency (float): Frequency of waves (in Hz).
            phases (list): Phase shifts for each transmitter (in degrees).
            curvature_angle (float): Curvature angle for curved arrays (in degrees).
        """
        c = 3e8  # Speed of light in m/s
        wavelength = c / frequency
        k = 2 * np.pi / wavelength  # Wave number

        # Grid for the plot in polar coordinates
        grid_size = 10
        r = np.linspace(0, grid_size / 2, 500)  # Radial distance
        theta = np.linspace(0, 2 * np.pi, 500)  # Angular range
        R, Theta = np.meshgrid(r, theta)

        # Convert polar to Cartesian coordinates
        X = R * np.cos(Theta)
        Y = R * np.sin(Theta)

        # Calculate transmitter positions
        if curvature_angle == 0:  # Linear array
            total_width = (num_transmitters - 1) * element_spacing
            positions_x = np.linspace(-total_width / 2, total_width / 2, num_transmitters)
            positions_y = np.zeros_like(positions_x)
        else:  # Curved array
            curvature = np.radians(curvature_angle)
            angles = np.linspace(-curvature / 2, curvature / 2, num_transmitters)
            positions_x = np.sin(angles) * (num_transmitters * element_spacing / curvature)
            positions_y = np.cos(angles) * (num_transmitters * element_spacing / curvature)

        # Initialize the field intensity map
        field_map = np.zeros_like(X, dtype=complex)

        # Compute the field map based on distance from each transmitter
        for i, (pos_x, pos_y) in enumerate(zip(positions_x, positions_y)):
            distance = np.sqrt((X - pos_x) ** 2 + (Y - pos_y) ** 2) + 1e-6  # Avoid division by zero
            phase_shift = np.radians(phases[i]) if i < len(phases) else 0
            wave = np.exp(1j * (k * distance + phase_shift))  # Wave amplitude
            field_map += wave

        # Calculate field intensity
        field_intensity = np.abs(field_map) ** 2
        normalized_field_intensity = (field_intensity - np.min(field_intensity)) / (
            np.max(field_intensity) - np.min(field_intensity)
        )

        # Plot the field map on a polar plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
        field_plot = ax.pcolormesh(Theta, R, normalized_field_intensity, cmap="RdBu_r", shading='auto')
        fig.colorbar(field_plot, ax=ax, label="Field Intensity (Normalized)")

        ax.set_title(f"Field Map ({num_transmitters} Transmitters, {frequency:.1f} Hz)", fontsize=14)

        return fig 

