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
            self.magnitudes = [1] * len(frequencies)  

    def set_phases(self, phases):
        self.phases = phases

    def set_array_type(self, array_type, curvature_angle):
        self.array_type = array_type
        self.curvature_angle = curvature_angle

    def calculate_positions(self):
        """
        Calculate element positions based on array type and curvature angle.
        """
        num_elements = len(self.frequencies)
        if self.array_type == "linear":
            return np.array([(n * self.element_spacing, 0) for n in range(num_elements)])
        else:  
            curvature = np.radians(self.curvature_angle)
            theta = np.linspace(-curvature / 2, curvature / 2, num_elements)
            return np.column_stack((np.sin(theta), np.cos(theta))) * num_elements * self.element_spacing

    def plot_beam_pattern_polar(self):
        num_elements = len(self.frequencies)
        if num_elements == 0:
            raise ValueError("No elements in the phased array for plotting beam pattern.")

        angles = np.linspace(0, np.pi, 360)
        k = 2 * np.pi / 1  # λ = 1 unit
        d = self.element_spacing / 1
        theta_0 = 0

        AF = np.zeros_like(angles, dtype=complex)
        for n in range(num_elements):
            beta = k * d * n * np.cos(angles - theta_0) + np.radians(self.phases[n])
            AF += self.magnitudes[n] * np.exp(1j * beta)

        AF = AF / num_elements
        AF_dB = 20 * np.log10(np.abs(AF) + 1e-12)

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 6))
        ax.plot(angles, AF_dB, color="blue", linewidth=2)
        ax.set_theta_zero_location("E")
        ax.set_theta_direction(1)
        ax.set_thetamin(0)
        ax.set_thetamax(180)
        ax.set_ylim(np.min(AF_dB) - 5, np.max(AF_dB) + 5)
        ax.set_title(f"Beam Pattern with {num_elements} Elements", va='bottom')
        ax.grid(True)
        return fig

    def plot_wave_propagation_pattern(self, num_transmitters, element_spacing, frequency, phases):
        """
        Plot the interference map for isotropic antennas in a phased array.

        Parameters:
            num_transmitters (int): Number of transmitters.
            element_spacing (float): Spacing between transmitters (in meters).
            frequency (float): Frequency of waves (in Hz).
            phases (list): Phases of the transmitters (in degrees).
        """
        # Constants
        c = 3e8  # Speed of light (m/s)
        wavelength = c / frequency  # Wavelength (m)
        k = 2 * np.pi / wavelength  # Wave number

        # Grid for the plot
        x = np.linspace(-5, 5, 1000)
        y = np.linspace(0, 5, 500)
        X, Y = np.meshgrid(x, y)
        interference_field = np.zeros_like(X, dtype=complex)

        # Transmitter positions
        total_width = (num_transmitters - 1) * element_spacing
        positions = np.linspace(-total_width / 2, total_width / 2, num_transmitters)

        # Calculate wave propagation for each transmitter
        for i, pos in enumerate(positions):
            distance = np.sqrt((X - pos) ** 2 + Y ** 2) + 1e-6  
            phase_shift = np.radians(phases[i]) if len(phases) > i else 0
            wave = np.exp(1j * (k * distance + phase_shift)) / distance  
            interference_field += wave

        # Normalize interference field
        interference_intensity = np.abs(interference_field) ** 2
        interference_intensity = (interference_intensity - np.min(interference_intensity)) / (
            np.max(interference_intensity) - np.min(interference_intensity)
        )

        # Create interference map plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.contourf(
            X,
            Y,
            interference_intensity,
            levels=300,
            cmap="viridis",
            alpha=0.9,
        )
        for pos in positions:
            ax.plot(pos, 0, 'ro', markersize=5)  # Plot transmitters as red dots
        ax.set_title("Interference Map", color="black", fontsize=14)
        ax.set_xlabel("X Position (m)", color="black")
        ax.set_ylabel("Y Position (m)", color="black")
        ax.tick_params(colors="black")
        ax.set_facecolor("black")
        ax.set_xlim(-5, 5)
        ax.set_ylim(0, 5)

        return fig
    