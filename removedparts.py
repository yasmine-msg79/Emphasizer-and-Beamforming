 

    # def plot_field_map(self, num_transmitters, element_spacing, frequency, phases):
    #     """
    #     Generate and plot a field map for the phased array.

    #     Parameters:
    #         num_transmitters (int): Number of transmitters.
    #         element_spacing (float): Spacing between transmitters (in meters).
    #         frequency (float): Frequency of waves (in Hz).
    #         phases (list): Phase shifts for each transmitter (in degrees).
    #     """
    #     c = 3e8  # Speed of light (m/s)
    #     wavelength = c / frequency
    #     k = 2 * np.pi / wavelength  # Wave number

    #     # Grid for the plot
    #     grid_size = 10  # Define the spatial range
    #     x = np.linspace(-grid_size / 2, grid_size / 2, 500)  # Higher resolution for fine details
    #     y = np.linspace(-grid_size / 2, grid_size / 2, 500)
    #     X, Y = np.meshgrid(x, y)

    #     # Calculate transmitter positions
    #     total_width = (num_transmitters - 1) * element_spacing
    #     positions = np.linspace(-total_width / 2, total_width / 2, num_transmitters)

    #     # Initialize the field
    #     field_map = np.zeros_like(X, dtype=complex)

    #     # Compute the field for each transmitter
    #     for i, pos in enumerate(positions):
    #         distance = np.sqrt((X - pos) ** 2 + Y ** 2) + 1e-6  # Avoid division by zero
    #         phase_shift = np.radians(phases[i]) if i < len(phases) else 0
    #         field_map += np.exp(1j * (k * distance + phase_shift)) / distance

    #     # Compute intensity
    #     field_intensity = np.abs(field_map)

    #     # Normalize the intensity
    #     field_intensity_normalized = (field_intensity - np.min(field_intensity)) / (
    #         np.max(field_intensity) - np.min(field_intensity)
    #     )

    #     # Plot the field map
    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     field_plot = ax.imshow(
    #         field_intensity_normalized,
    #         extent=(-grid_size / 2, grid_size / 2, -grid_size / 2, grid_size / 2),
    #         cmap="RdBu_r",
    #         origin="lower",
    #         interpolation="none",
    #     )
    #     fig.colorbar(field_plot, ax=ax, label="Field Intensity")
        
    #     # Overlay transmitter positions
    #     for pos in positions:
    #         ax.plot(pos, 0, 'ro', markersize=5, label="Transmitter")
        
    #     ax.set_title(f"Field Map ({num_transmitters} Transmitters, {frequency:.1f} Hz)", fontsize=14)
    #     ax.set_xlabel("X Position (m)")
    #     ax.set_ylabel("Y Position (m)")
    #     ax.legend()
        
    #     return fig

    # def plot_field_map(self, num_transmitters, element_spacing, frequency, phases):
    #     """
    #     Generate and plot a field map based on the wavelength difference from transmitters.

    #     Parameters:
    #         num_transmitters (int): Number of transmitters.
    #         element_spacing (float): Spacing between transmitters (in meters).
    #         frequency (float): Frequency of waves (in Hz).
    #         phases (list): Phase shifts for each transmitter (in degrees).
    #     """
    #     c = 3e8  # Speed of light (m/s)
    #     wavelength = c / frequency
    #     k = 2 * np.pi / wavelength  # Wave number

    #     # Grid for the plot
    #     grid_size = 10  # Spatial range
    #     x = np.linspace(-grid_size / 2, grid_size / 2, 500)  # Higher resolution for better detail
    #     y = np.linspace(-grid_size / 2, grid_size / 2, 500)
    #     X, Y = np.meshgrid(x, y)

    #     # Calculate transmitter positions
    #     total_width = (num_transmitters - 1) * element_spacing
    #     positions = np.linspace(-total_width / 2, total_width / 2, num_transmitters)

    #     # Initialize the field intensity map
    #     field_map = np.zeros_like(X, dtype=complex)

    #     # Compute the field map based on distance from each transmitter
    #     for i, pos in enumerate(positions):
    #         distance = np.sqrt((X - pos) ** 2 + Y ** 2) + 1e-6  # Avoid division by zero
    #         phase_shift = np.radians(phases[i]) if i < len(phases) else 0
    #         wave = np.exp(1j * (k * distance + phase_shift))  # Wave amplitude
    #         field_map += wave

    #     # Calculate wavelength difference
    #     field_intensity = np.abs(field_map) ** 2  # Intensity proportional to the square of amplitude
    #     normalized_field_intensity = (field_intensity - np.min(field_intensity)) / (
    #         np.max(field_intensity) - np.min(field_intensity)
    #     )

    #     # Plot the field map
    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     field_plot = ax.imshow(
    #         normalized_field_intensity,
    #         extent=(-grid_size / 2, grid_size / 2, -grid_size / 2, grid_size / 2),
    #         cmap="RdBu_r",
    #         origin="lower",
    #         interpolation="none",
    #     )
    #     fig.colorbar(field_plot, ax=ax, label="Field Intensity (Normalized)")

    #     # Overlay transmitter positions
    #     for pos in positions:
    #         ax.plot(pos, 0, 'ro', markersize=5, label="Transmitter")

    #     ax.set_title(f"Field Map ({num_transmitters} Transmitters, {frequency:.1f} Hz)", fontsize=14)
    #     ax.set_xlabel("X Position (m)")
    #     ax.set_ylabel("Y Position (m)")
    #     ax.legend()
        
    #     return fig







    # def plot_beam_pattern_polar(self):
    #     num_elements = len(self.frequencies)
    #     if num_elements == 0:
    #         raise ValueError("No elements in the phased array for plotting beam pattern.")

    #     # Angular range for the plot (0° to 180°)
    #     angles = np.linspace(0, np.pi, 360)  # From 0° to 180° in radians
    #     c = 3e8  # Speed of light in m/s
    #     wavelength = c / self.frequencies[0]  # Wavelength based on the first frequency
    #     k = 2 * np.pi / wavelength  # Wave number
    #     d = self.element_spacing * wavelength  # Element spacing in terms of wavelength

    #     print(f"Frequency: {self.frequencies[0]} Hz")
    #     print(f"Wavelength: {wavelength:.3e} m")
    #     print(f"Element Spacing: {d:.3e} m")

    #     # Introduce an overall rotation factor based on phase shift
    #     rotation_phase = np.radians(self.phases[0])  # Use the first phase for simplicity
    #     rotated_angles = angles + rotation_phase

    #     # Calculate the Array Factor (AF)
    #     AF = np.zeros_like(angles, dtype=complex)
    #     for n in range(num_elements):
    #         beta = k * d * n * np.cos(rotated_angles) + np.radians(self.phases[n])
    #         AF += self.magnitudes[n] * np.exp(1j * beta)

    #     # Normalize AF and convert to dB
    #     AF = AF / num_elements
    #     AF_dB = 20 * np.log10(np.abs(AF) + 1e-12)

    #     # Create the polar plot
    #     fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 6))
    #     ax.plot(angles, AF_dB, color="blue", linewidth=2)
    #     ax.set_theta_zero_location("E")  # East as 0 degrees (horizontal line on the right)
    #     ax.set_theta_direction(1)  # Anti-clockwise direction
    #     ax.set_thetamin(0)  # Start at 0 degrees (horizontal line on the right)
    #     ax.set_thetamax(180)  # End at 180 degrees (horizontal line on the left)
    #     ax.set_ylim(np.min(AF_dB) - 5, np.max(AF_dB) + 5)  # Dynamic range
    #     ax.set_title(f"Beam Pattern with {num_elements} Elements", va='bottom')
    #     ax.grid(True)
    #     return fig

def plot_beam_pattern_polar(self, num_transmitters, element_spacing, frequency, phases, curvature_angle):
        """
        Generate and plot a full-circle beam pattern.

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

        # Angular range for the full-circle plot (0° to 360°)
        angles = np.linspace(0, 2 * np.pi, 360)

        # Calculate transmitter positions based on curvature angle
        if curvature_angle == 0:  # Linear array
            total_width = (num_transmitters - 1) * element_spacing
            positions_x = np.linspace(-total_width / 2, total_width / 2, num_transmitters)
            positions_y = np.zeros_like(positions_x)
        else:  # Curved array
            curvature = np.radians(curvature_angle)
            element_arc = (num_transmitters * element_spacing) / curvature
            angles_curve = np.linspace(-element_arc / 2, element_arc / 2, num_transmitters)
            positions_x = np.sin(angles_curve) * element_arc
            positions_y = np.cos(angles_curve) * element_arc

        # Calculate the beam intensity for each angle
        AF = np.zeros_like(angles, dtype=complex)
        for i, (pos_x, pos_y) in enumerate(zip(positions_x, positions_y)):
            for j, angle in enumerate(angles):
                x = np.cos(angle)  # Direction vector x
                y = np.sin(angle)  # Direction vector y
                projection = pos_x * x + pos_y * y  # Projection of element position on the direction
                phase_shift = np.radians(phases[i]) if i < len(phases) else 0
                AF[j] += np.exp(1j * (k * projection + phase_shift))

        # Normalize and convert to dB
        AF = np.abs(AF) / num_transmitters
        AF_dB = 20 * np.log10(AF + 1e-12)

        # Create the polar plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(5, 5))
        ax.plot(angles, AF_dB, color="blue", linewidth=2)
        ax.set_theta_zero_location("E")  # East as 0 degrees
        ax.set_theta_direction(1)  # Anti-clockwise direction
        ax.set_ylim(np.min(AF_dB) - 5, np.max(AF_dB) + 5)  # Dynamic range
        ax.set_title(f"Beam Pattern ({num_transmitters} Elements, {frequency:.1f} Hz)", va='bottom')
        ax.grid(True)

        return fig

    