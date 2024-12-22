import numpy as np
import cv2

class Mixer:
    def __init__(self, ft_components, rects, min_width, min_height, used_width, used_height, magnitude_phase, rectangle, checkboxes, weights_sliders, current_images):
        self.ft_components = ft_components
        self.rects = rects
        self.min_width = min_width
        self.min_height = min_height
        self.used_width = used_width
        self.used_height = used_height
        self.magnitude_phase = magnitude_phase
        self.rectangle = rectangle
        self.checkboxes = checkboxes
        self.weights_sliders = weights_sliders
        self.current_images = current_images
        self.weights = [0, 0, 0, 0]
        
    def compute_inverse_ft_components(self):
        reconstructed_image = None
        magnitude_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Magnitude" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]
        phase_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Phase" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]
        real_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Real" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]
        imaginary_weights = [
            slider.value() / 100 if combobox.currentText() == "FT Imaginary" else 0
            for slider, combobox in zip(self.weights_sliders, self.checkboxes)
        ]

        if self.magnitude_phase.isChecked():
            ft_magnitude_sum = np.zeros((self.min_height, self.min_width))
            ft_phase_sum = np.zeros((self.min_height, self.min_width))

            for i in range(len(self.ft_components)):
                if self.current_images[i] is not None:
                    x_min = self.rects[i].x_min
                    x_max = self.rects[i].x_max
                    y_min = self.rects[i].y_min
                    y_max = self.rects[i].y_max

                    x_min, x_max = max(0, x_min), min(self.used_width, x_max)
                    y_min, y_max = max(0, y_min), min(self.used_height, y_max)

                    if self.in_region_radioButton.isChecked():
                        mask = np.zeros((self.used_width, self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 1
                    else:
                        mask = np.ones((self.used_width, self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 0

                    mask = cv2.resize(mask, (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_magnitude = cv2.resize(self.ft_components[i]["FT Magnitude"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_phase = cv2.resize(self.ft_components[i]["FT Phase"], (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)

                    ft_magnitude_sum += resized_magnitude * magnitude_weights[i] 
                    ft_phase_sum += resized_phase * phase_weights[i]

            reconstructed_ft = np.multiply(np.expm1(ft_magnitude_sum), np.exp(1j * ft_phase_sum))
            reconstructed_ft *= mask
            reconstructed_image = np.abs(np.fft.ifft2(np.fft.ifftshift(reconstructed_ft)))

        else:
            ft_real_sum = np.zeros((self.min_height, self.min_width))
            ft_imaginary_sum = np.zeros((self.min_height, self.min_width))

            rect_bounds = self.rectangle.sceneBoundingRect()
            x_min, y_min = int(rect_bounds.left()), int(rect_bounds.top())
            x_max, y_max = int(rect_bounds.right()), int(rect_bounds.bottom())

            for i in range(len(self.ft_components)):
                if self.current_images[i] is not None:
                    x_min = self.rects[i].x_min
                    x_max = self.rects[i].x_max
                    y_min = self.rects[i].y_min
                    y_max = self.rects[i].y_max

                    x_min, x_max = max(0, x_min), min(self.used_width, x_max)
                    y_min, y_max = max(0, y_min), min(self.used_height, y_max)

                    if self.in_region_radioButton.isChecked():
                        mask = np.zeros((self.used_width, self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 1
                    else:
                        mask = np.ones((self.used_width, self.used_height), dtype=np.uint8)
                        mask[y_min:y_max, x_min:x_max] = 0

                    mask = cv2.resize(mask, (self.min_width, self.min_height), interpolation=cv2.INTER_LINEAR)
                    resized_real = self.ft_components[i]["FT Real"].reshape(self.min_height, self.min_width)
                    resized_imaginary = self.ft_components[i]["FT Imaginary"].reshape(self.min_height, self.min_width)
                    ft_real_sum += resized_real * real_weights[i] * mask
                    ft_imaginary_sum += resized_imaginary * imaginary_weights[i] * mask

            mixed_image = np.fft.ifft2(ft_real_sum + 1j * ft_imaginary_sum)
            reconstructed_image = np.abs(mixed_image)

        if reconstructed_image is not None:
            max_val = np.max(reconstructed_image)
            reconstructed_image = (255 * (reconstructed_image / max_val)).astype(np.uint8) if max_val > 0 else np.zeros_like(reconstructed_image, dtype=np.uint8)

        return reconstructed_image

    def update_weight(self, frame, value):
        self.weights[frame] = value
        return self.compute_inverse_ft_components()
