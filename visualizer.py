import numpy as np
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self):
        self.frequencies = []
        self.phases = []
        self.array_type = "linear"
        self.curvature_angle = 0.0
        self.element_spacing = 0.5  # Default spacing in wavelength units

    def set_frequencies(self, frequencies):
        self.frequencies = frequencies

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
            # Linear array along the x-axis
            return np.array([(n * self.element_spacing, 0) for n in range(num_elements)])
        else:  # Curved array
            curvature = np.radians(self.curvature_angle)
            theta = np.linspace(-curvature / 2, curvature / 2, num_elements)
            return np.column_stack((np.sin(theta), np.cos(theta))) * num_elements * self.element_spacing


    def plot_beam_pattern(self):
            """
            Generate and return the heatmap for the beamforming pattern.
            """
            import numpy as np
            import matplotlib.pyplot as plt

            k = 2 * np.pi  # Wavenumber (normalized for simplicity)

            # Calculate element positions
            positions = self.calculate_positions()

            # Spatial grid
            x = np.linspace(-2, 2, 300)
            y = np.linspace(-2, 2, 300)
            X, Y = np.meshgrid(x, y)
            field = np.zeros_like(X, dtype=complex)

            # Sum contributions from all elements
            for (px, py), freq, phase in zip(positions, self.frequencies, self.phases):
                r = np.sqrt((X - px)**2 + (Y - py)**2)
                field += np.exp(1j * (k * r + np.radians(phase)))

            # Calculate intensity
            intensity = np.abs(field)**2

            # Plot heatmap
            fig, ax = plt.subplots(figsize=(6, 6))
            c = ax.contourf(X, Y, intensity, levels=50, cmap="viridis")
            fig.colorbar(c, ax=ax).set_label("Signal Intensity")
            ax.set_title("Beamforming Heatmap")
            ax.set_xlabel("X (wavelength units)")
            ax.set_ylabel("Y (wavelength units)")
            return fig

    def plot_phase_magnitude(self):
        """
        Generate and return the phase-magnitude plot for the transmitters.
        """
        import matplotlib.pyplot as plt

        num_elements = len(self.frequencies)
        if num_elements == 0:
            raise ValueError("No elements in the phased array for plotting phase-magnitude.")

        # Generate data for plotting
        x = range(1, num_elements + 1)  # Transmitter indices
        phases = self.phases  # Phases (degrees)
        magnitudes = [1] * num_elements  # Magnitudes are typically uniform (can be adjusted)

        # Plot the phase vs. magnitude
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, phases, label="Phase (degrees)", marker="o")
        ax.stem(x, magnitudes, linefmt="g-", markerfmt="go", basefmt="r-", label="Magnitude")

        # Add labels and title
        ax.set_title("Phase vs Magnitude")
        ax.set_xlabel("Transmitter Index")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)

        return fig
