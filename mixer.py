import numpy as np
import cv2

class Mixer:
    def __init__(self, sliders, rectangles, ft_components, min_width, min_height, region_callbacks):
        self.weights = [0, 0, 0, 0]
        self.sliders = sliders
        self.rectangles = rectangles
        self.ft_components = ft_components
        self.min_width = min_width
        self.min_height = min_height
        self.region_callbacks = region_callbacks
        self.region_mask = None

        # Connect sliders to weight update
        for idx, slider in enumerate(self.sliders):
            slider.valueChanged.connect(lambda value, i=idx: self.update_weight(i, value))

    def update_weight(self, index, value):
        """Update the weight for the given index when the slider value changes."""
        self.weights[index] = value / 100

    def compute_region_mask(self, rect, in_region):
        """Generate a mask based on the selected region."""
        x_min, x_max = max(0, rect.x_min), min(self.min_width, rect.x_max)
        y_min, y_max = max(0, rect.y_min), min(self.min_height, rect.y_max)

        mask = np.zeros((self.min_width, self.min_height), dtype=np.uint8)
        if in_region:
            mask[y_min:y_max, x_min:x_max] = 1
        else:
            mask[:, :] = 1
            mask[y_min:y_max, x_min:x_max] = 0

        return mask

    def compute_inverse_ft(self, use_magnitude_phase, in_region):
        """Reconstruct the image based on the current FT components and weights."""
        if use_magnitude_phase:
            magnitude_sum = np.zeros((self.min_height, self.min_width), dtype=np.complex128)
            phase_sum = np.zeros((self.min_height, self.min_width), dtype=np.complex128)

            for idx, rect in enumerate(self.rectangles):
                if self.ft_components[idx]:
                    mask = self.compute_region_mask(rect, in_region)
                    resized_magnitude = cv2.resize(self.ft_components[idx]["FT Magnitude"], 
                                                   (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_phase = cv2.resize(self.ft_components[idx]["FT Phase"], 
                                                (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)

                    magnitude_sum += resized_magnitude * self.weights[idx]
                    phase_sum += np.exp(1j * resized_phase) * self.weights[idx]

            reconstructed_ft = np.multiply(np.expm1(magnitude_sum), np.exp(1j * np.angle(phase_sum)))
            reconstructed_ft *= mask
        else:
            real_sum = np.zeros((self.min_height, self.min_width))
            imaginary_sum = np.zeros((self.min_height, self.min_width))

            for idx, rect in enumerate(self.rectangles):
                if self.ft_components[idx]:
                    mask = self.compute_region_mask(rect, in_region)
                    resized_real = cv2.resize(self.ft_components[idx]["FT Real"], 
                                              (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_imaginary = cv2.resize(self.ft_components[idx]["FT Imaginary"], 
                                                   (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)

                    real_sum += resized_real * self.weights[idx] * mask
                    imaginary_sum += resized_imaginary * self.weights[idx] * mask

            reconstructed_ft = real_sum + 1j * imaginary_sum

        # Reconstruct image from inverse FT
        reconstructed_image = np.fft.ifft2(reconstructed_ft)
        reconstructed_image = np.abs(reconstructed_image)

        # Normalize to 8-bit range
        max_val = np.max(reconstructed_image)
        if max_val > 0:
            reconstructed_image = (255 * (reconstructed_image / max_val)).astype(np.uint8)
        else:
            reconstructed_image = np.zeros_like(reconstructed_image, dtype=np.uint8)

        return reconstructed_image

    def on_region_changed(self, in_region):
        """Handle region changes triggered by external UI controls."""
        self.region_mask = in_region
        if self.region_callbacks:
            for callback in self.region_callbacks:
                callback()
