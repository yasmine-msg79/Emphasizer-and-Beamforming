# class Visualizer:
#     def __init__(self):
#         self.frequencies = [] 
#         self.phases = []  
#         self.magnitudes = []  
#         self.array_type = "linear"  
#         self.curvature_angle = 0.0  
#         self.element_spacing = 0.5  

#     def set_frequencies(self, frequencies):
#         self.frequencies = frequencies
#         if len(self.magnitudes) < len(frequencies):
#             self.magnitudes = [1] * len(frequencies) 
#         print(f"self.frequencies in visualizer: {self.frequencies}")
         

#     def set_phases(self, phases):
#         self.phases = phases
#         print(f"self.phases in visualizer: {self.phases}")


#     def set_array_type(self, array_type, curvature_angle):
#         self.array_type = array_type
#         self.curvature_angle = curvature_angle
#         print(f"self.array_type in visualizer : {self.array_type}")
#         print(f"self.curvature_angle in visualizer : {self.curvature_angle}")

#     def calculate_positions(self, num_elements):
#         if self.array_type == "linear":
#             x_positions = np.linspace(-num_elements * self.element_spacing / 2,
#                                        num_elements * self.element_spacing / 2,
#                                        num_elements)
#             y_positions = np.zeros_like(x_positions)
#         else:
#             curvature = np.radians(self.curvature_angle)
#             theta = np.linspace(-curvature / 2, curvature / 2, num_elements)
#             radius = num_elements * self.element_spacing / curvature if curvature != 0 else 0
#             x_positions = radius * np.sin(theta)
#             y_positions = radius * np.cos(theta)
#         return x_positions, y_positions

    
#     def plot_field_map(self, num_transmitters, element_spacing, frequency, phases, curvature_angle):
#         """
#         Generate and plot a heat map in polar coordinates showing constructive and destructive interference.

#         Parameters:
#             num_transmitters (int): Number of transmitters.
#             element_spacing (float): Spacing between transmitters (in meters).
#             frequency (float): Frequency of waves (in Hz).
#             phases (list): Phase shifts for each transmitter (in degrees).
#             curvature_angle (float): Curvature angle for curved arrays (in degrees).
#         """
#         c = 3e8  # Speed of light (m/s)
#         wavelength = c / frequency
#         k = 2 * np.pi / wavelength  # Wave number

#         # Calculate transmitter positions based on curvature angle
#         if curvature_angle == 0:  # Linear array
#             total_width = (num_transmitters - 1) * element_spacing
#             positions_x = np.linspace(-total_width / 2, total_width / 2, num_transmitters)
#             positions_y = np.zeros_like(positions_x)
#         else:  # Curved array
#             curvature = np.radians(curvature_angle)
#             angles = np.linspace(-curvature / 2, curvature / 2, num_transmitters)
#             radius = num_transmitters * element_spacing / curvature
#             positions_x = radius * np.sin(angles)
#             positions_y = radius * (1 - np.cos(angles))

#         # Define grid for heat map calculation in polar coordinates
#         grid_size = 500  # Number of points along one axis
#         r = np.linspace(0, 15, grid_size)
#         theta = np.linspace(0, 2 * np.pi, grid_size)
#         R, Theta = np.meshgrid(r, theta)

#         # Convert polar grid to Cartesian coordinates
#         X = R * np.cos(Theta)
#         Y = R * np.sin(Theta)

#         # Initialize the heat map
#         heat_map = np.zeros_like(X, dtype=complex)

#         # Compute the heat map based on interference from each transmitter
#         for i, (pos_x, pos_y) in enumerate(zip(positions_x, positions_y)):
#             distance = np.sqrt((X - pos_x) ** 2 + (Y - pos_y) ** 2) + 1e-6  # Avoid division by zero
#             phase_shift = np.radians(phases[i]) if i < len(phases) else 0
#             wave = np.exp(1j * (k * distance + phase_shift))
#             heat_map += wave

#         # Calculate interference pattern intensity
#         intensity = np.abs(heat_map) ** 2

#         # Normalize intensity for consistency with beam pattern
#         intensity /= np.max(intensity)

#         # Adjust phase contribution to match beam pattern logic by rotating the intensity
#         if phases:
#             total_phase_shift = np.mean(np.radians(phases))
#             theta_shift = int(total_phase_shift / (2 * np.pi) * grid_size)
#             intensity = np.roll(intensity, shift=theta_shift, axis=0)

#         # Plot the heat map in polar coordinates
#         fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
#         heat_plot = ax.pcolormesh(Theta, R, intensity, cmap="viridis", shading="auto")
#         fig.colorbar(heat_plot, ax=ax, label="Interference Intensity")

#         # Overlay transmitter positions
#         transmitter_r = np.sqrt(positions_x**2 + positions_y**2)
#         transmitter_theta = np.arctan2(positions_y, positions_x)
#         ax.plot(transmitter_theta, transmitter_r, 'ro', markersize=5)  # Transmitter markers

#         ax.set_title(f"Heat Map in Polar Coordinates ({num_transmitters} Transmitters, {frequency:.1f} Hz)", fontsize=14)
#         ax.set_rlabel_position(-22.5)  # Move radial labels to avoid overlap

#         return fig

#     def plot_beam_pattern_polar(self, num_transmitters, element_spacing, frequency, phases, curvature_angle):
#         """
#         Generate and plot the beam pattern in polar coordinates, reflecting the intensity and directionality
#         of the transmitted signals based on frequency, phases, and curvature angle.

#         Parameters:
#             num_transmitters (int): Number of transmitters.
#             element_spacing (float): Spacing between transmitters (in meters).
#             frequency (float): Frequency of waves (in Hz).
#             phases (list): Phase shifts for each transmitter (in degrees).
#             curvature_angle (float): Curvature angle for curved arrays (in degrees).
#         """
#         c = 3e8  # Speed of light (m/s)
#         wavelength = c / frequency
#         k = 2 * np.pi / wavelength  # Wave number

#         # Calculate transmitter positions based on curvature angle
#         if curvature_angle == 0:  # Linear array
#             total_width = (num_transmitters - 1) * element_spacing
#             positions_x = np.linspace(-total_width / 2, total_width / 2, num_transmitters)
#             positions_y = np.zeros_like(positions_x)
#         else:  # Curved array
#             curvature = np.radians(curvature_angle)
#             angles = np.linspace(-curvature / 2, curvature / 2, num_transmitters)
#             radius = num_transmitters * element_spacing / curvature
#             positions_x = radius * np.sin(angles)
#             positions_y = radius * (1 - np.cos(angles))

#         # Define angular range for beam pattern calculation
#         theta = np.linspace(0, 2 * np.pi, 360)
#         angles = np.linspace(0, 2 * np.pi, 360)  # Angular directions

#         # Initialize the beam pattern
#         beam_pattern = np.zeros_like(angles, dtype=complex)

#         # Compute the beam pattern based on contributions from each transmitter
#         for i, (pos_x, pos_y) in enumerate(zip(positions_x, positions_y)):
#             for idx, angle in enumerate(angles):
#                 x = pos_x * np.cos(angle) + pos_y * np.sin(angle)
#                 phase_shift = np.radians(phases[i]) if i < len(phases) else 0
#                 wave = np.exp(1j * (k * x + phase_shift))
#                 beam_pattern[idx] += wave

#         # Calculate intensity of the beam pattern
#         intensity = np.abs(beam_pattern) ** 2

#         # Normalize intensity for consistency
#         intensity /= np.max(intensity)

#         # Apply phase rotation to match the heat map logic
#         if phases:
#             total_phase_shift = np.mean(np.radians(phases))
#             theta_shift = int(total_phase_shift / (2 * np.pi) * len(angles))
#             intensity = np.roll(intensity, shift=theta_shift)

#         # Create the polar plot
#         fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
#         ax.plot(angles, intensity, color="blue", linewidth=2)

#         ax.set_title(f"Beam Pattern ({num_transmitters} Transmitters, {frequency:.1f} Hz)", fontsize=14)
#         ax.grid(True)

#         return fig






# class Visualizer:
#     def __init__(self):
#         self.frequencies = [] 
#         self.phases = []  
#         self.magnitudes = []  
#         self.array_type = "linear"  
#         self.curvature_angle = 0.0  
#         self.element_spacing = 0.5  
#         self.position_offset = [0, 0]  # Default position offset (x, y)

#     def set_frequencies(self, frequencies):
#         self.frequencies = frequencies
#         if len(self.magnitudes) < len(frequencies):
#             self.magnitudes = [1] * len(frequencies) 
#         print(f"self.frequencies in visualizer: {self.frequencies}")

#     def set_phases(self, phases):
#         self.phases = phases
#         print(f"self.phases in visualizer: {self.phases}")

#     def set_array_type(self, array_type, curvature_angle):
#         self.array_type = array_type
#         self.curvature_angle = curvature_angle
#         print(f"self.array_type in visualizer : {self.array_type}")
#         print(f"self.curvature_angle in visualizer : {self.curvature_angle}")

#     def set_position_offset(self, offset_x, offset_y):
#         self.position_offset = [offset_x, offset_y]
#         print(f"self.position_offset: {self.position_offset}")

#     def calculate_positions(self, num_elements):
#         """
#         Calculate the positions of the transmitters based on the array type (linear/curved),
#         curvature angle, and the position offset.
#         """
#         if self.array_type == "linear":
#             # Linear array positions
#             x_positions = np.linspace(-num_elements * self.element_spacing / 2,
#                                     num_elements * self.element_spacing / 2,
#                                     num_elements)
#             y_positions = np.zeros_like(x_positions)
#         else:
#             # Curved array positions
#             curvature = np.radians(self.curvature_angle)
#             theta = np.linspace(-curvature / 2, curvature / 2, num_elements)
#             radius = (num_elements * self.element_spacing) / curvature if curvature != 0 else 0

#             # Calculate positions on the arc
#             x_positions = radius * np.sin(theta)
#             y_positions = -radius * (1 - np.cos(theta))  # Negative for arc facing downward

#         # Apply position offset
#         x_positions += self.position_offset[0]
#         y_positions += self.position_offset[1]

#         return x_positions, y_positions

#     def plot_field_map(self, num_transmitters, element_spacing, frequency, phases, curvature_angle):
#         # Existing logic
#         c = 3e8  # Speed of light (m/s)
#         wavelength = c / frequency
#         k = 2 * np.pi / wavelength  # Wave number

#         # Calculate transmitter positions with offset
#         positions_x, positions_y = self.calculate_positions(num_transmitters)

#         # Define grid for heat map calculation in polar coordinates
#         grid_size = 500  # Number of points along one axis
#         r = np.linspace(0, 15, grid_size)
#         theta = np.linspace(0, 2 * np.pi, grid_size)
#         R, Theta = np.meshgrid(r, theta)

#         # Convert polar grid to Cartesian coordinates
#         X = R * np.cos(Theta)
#         Y = R * np.sin(Theta)

#         # Initialize the heat map
#         heat_map = np.zeros_like(X, dtype=complex)

#         # Compute the heat map based on interference from each transmitter
#         for i, (pos_x, pos_y) in enumerate(zip(positions_x, positions_y)):
#             distance = np.sqrt((X - pos_x) ** 2 + (Y - pos_y) ** 2) + 1e-6  # Avoid division by zero
#             phase_shift = np.radians(phases[i]) if i < len(phases) else 0
#             wave = np.exp(1j * (k * distance + phase_shift))
#             heat_map += wave

#         # Calculate interference pattern intensity
#         intensity = np.abs(heat_map) ** 2

#         # Normalize intensity for consistency with beam pattern
#         intensity /= np.max(intensity)

#         # Adjust phase contribution to match beam pattern logic by rotating the intensity
#         if phases:
#             total_phase_shift = np.mean(np.radians(phases))
#             theta_shift = int(total_phase_shift / (2 * np.pi) * grid_size)
#             intensity = np.roll(intensity, shift=theta_shift, axis=0)

#         # Plot the heat map in polar coordinates
#         fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
#         heat_plot = ax.pcolormesh(Theta, R, intensity, cmap="viridis", shading="auto")
#         fig.colorbar(heat_plot, ax=ax, label="Interference Intensity")

#         # Overlay transmitter positions
#         transmitter_r = np.sqrt(positions_x**2 + positions_y**2)
#         transmitter_theta = np.arctan2(positions_y, positions_x)
#         ax.plot(transmitter_theta, transmitter_r, 'ro', markersize=5)  # Transmitter markers

#         ax.set_title(f"Heat Map in Polar Coordinates ({num_transmitters} Transmitters, {frequency:.1f} Hz)", fontsize=14)
#         ax.set_rlabel_position(-22.5)  # Move radial labels to avoid overlap

#         return fig


#     def plot_beam_pattern_polar(self, num_transmitters, element_spacing, frequency, phases, curvature_angle):
#         # Existing logic
#         c = 3e8  # Speed of light (m/s)
#         wavelength = c / frequency
#         k = 2 * np.pi / wavelength  # Wave number

#         # Calculate transmitter positions with offset
#         positions_x, positions_y = self.calculate_positions(num_transmitters)

#         # Define angular range for beam pattern calculation
#         angles = np.linspace(0, 2 * np.pi, 360)  # Angular directions

#         # Initialize the beam pattern
#         beam_pattern = np.zeros_like(angles, dtype=complex)

#         # Compute the beam pattern based on contributions from each transmitter
#         for i, (pos_x, pos_y) in enumerate(zip(positions_x, positions_y)):
#             for idx, angle in enumerate(angles):
#                 x = pos_x * np.cos(angle) + pos_y * np.sin(angle)
#                 phase_shift = np.radians(phases[i]) if i < len(phases) else 0
#                 wave = np.exp(1j * (k * x + phase_shift))
#                 beam_pattern[idx] += wave

#         # Calculate intensity of the beam pattern
#         intensity = np.abs(beam_pattern) ** 2

#         # Normalize intensity for consistency
#         intensity /= np.max(intensity)

#         # Apply phase rotation to match the heat map logic
#         if phases:
#             total_phase_shift = np.mean(np.radians(phases))
#             theta_shift = int(total_phase_shift / (2 * np.pi) * len(angles))
#             intensity = np.roll(intensity, shift=theta_shift)

#         # Create the polar plot
#         fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
#         ax.plot(angles, intensity, color="blue", linewidth=2)

#         ax.set_title(f"Beam Pattern ({num_transmitters} Transmitters, {frequency:.1f} Hz)", fontsize=14)
#         ax.grid(True)

#         return fig
