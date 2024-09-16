class StructuralSimilarityIndex:
    def __init__(self, k1=0.01, k2=0.03, L=255):
        """
        Initialize SSIM parameters.
        k1, k2: Constants to stabilize the formula
        L: Dynamic range of the pixel values (255 for 8-bit grayscale images)
        """
        self.C1 = (k1 * L) ** 2
        self.C2 = (k2 * L) ** 2

    def mean(self, image):
        """
        Calculate the mean pixel value of an image.
        :param image: 2D list representing a grayscale image
        :return: Mean of pixel intensities
        """
        total = 0
        count = 0
        for row in image:
            total += sum(row)
            count += len(row)
        return total / count

    def variance(self, image, mean):
        """
        Calculate the variance of pixel intensities in an image.
        :param image: 2D list representing a grayscale image
        :param mean: Mean pixel intensity
        :return: Variance of pixel intensities
        """
        total = 0
        count = 0
        for row in image:
            for pixel in row:
                total += (pixel - mean) ** 2
            count += len(row)
        return total / count

    def covariance(self, image1, image2, mean1, mean2):
        """
        Calculate the covariance between two images.
        :param image1: 2D list representing the first grayscale image
        :param image2: 2D list representing the second grayscale image
        :param mean1: Mean pixel intensity of the first image
        :param mean2: Mean pixel intensity of the second image
        :return: Covariance between the two images
        """
        total = 0
        count = 0
        for i in range(len(image1)):
            for j in range(len(image1[0])):
                total += (image1[i][j] - mean1) * (image2[i][j] - mean2)
            count += len(image1[i])
        return total / count

    def ssim(self, image1, image2):
        """
        Calculate the SSIM between two images.
        :param image1: 2D list representing the first grayscale image
        :param image2: 2D list representing the second grayscale image
        :return: SSIM value
        """
        # Step 1: Calculate mean for both images
        mean1 = self.mean(image1)
        mean2 = self.mean(image2)

        # Step 2: Calculate variance for both images
        variance1 = self.variance(image1, mean1)
        variance2 = self.variance(image2, mean2)

        # Step 3: Calculate covariance between the two images
        covariance12 = self.covariance(image1, image2, mean1, mean2)

        # Step 4: Calculate SSIM based on the formula
        numerator1 = (2 * mean1 * mean2 + self.C1)
        numerator2 = (2 * covariance12 + self.C2)
        denominator1 = (mean1 ** 2 + mean2 ** 2 + self.C1)
        denominator2 = (variance1 + variance2 + self.C2)

        ssim_value = (numerator1 * numerator2) / (denominator1 * denominator2)
        return ssim_value

    def example(self):
        """
        Example usage with two small 3x3 grayscale images.
        """
        image1 = [
            [52, 55, 61],
            [54, 56, 62],
            [58, 59, 63]
        ]
        
        image2 = [
            [52, 54, 60],
            [53, 55, 61],
            [57, 58, 62]
        ]

        ssim_score = self.ssim(image1, image2)
        print(f"SSIM between example images: {ssim_score:.4f}")

import math

class PeakSignalToNoiseRatio:
    def __init__(self, max_pixel_value=255):
        """
        Initialize the PSNR calculator.
        
        :param max_pixel_value: Maximum possible pixel value (255 for 8-bit grayscale images)
        """
        self.max_pixel_value = max_pixel_value

    def mean_squared_error(self, image1, image2):
        """
        Calculate the Mean Squared Error (MSE) between two images.
        
        :param image1: 2D list representing the first grayscale image
        :param image2: 2D list representing the second grayscale image
        :return: Mean Squared Error (MSE) between the two images
        """
        if len(image1) != len(image2) or len(image1[0]) != len(image2[0]):
            raise ValueError("Images must have the same dimensions")

        error_sum = 0
        total_pixels = len(image1) * len(image1[0])

        for i in range(len(image1)):
            for j in range(len(image1[0])):
                error_sum += (image1[i][j] - image2[i][j]) ** 2

        return error_sum / total_pixels

    def psnr(self, image1, image2):
        """
        Calculate the PSNR between two images.
        
        :param image1: 2D list representing the first grayscale image
        :param image2: 2D list representing the second grayscale image
        :return: PSNR value in dB
        """
        mse = self.mean_squared_error(image1, image2)

        if mse == 0:
            return float('inf')  # Infinite PSNR if the images are identical

        psnr_value = 10 * math.log10((self.max_pixel_value ** 2) / mse)
        return psnr_value

    def example(self):
        """
        Example usage of PSNR with two 3x3 grayscale images.
        """
        image1 = [
            [52, 55, 61],
            [54, 56, 62],
            [58, 59, 63]
        ]
        
        image2 = [
            [52, 54, 60],
            [53, 55, 61],
            [57, 58, 62]
        ]

        psnr_value = self.psnr(image1, image2)
        print(f"PSNR between example images: {psnr_value:.2f} dB")

class HistogramIntersection:
    # Static variables for histogram bins (initialized to empty)
    hist1 = []
    hist2 = []

    def __init__(self):
        """
        Initializes the HistogramIntersection class.
        """
        pass

    @staticmethod
    def set_histograms(histogram1, histogram2):
        """
        Set the static histograms for comparison.
        
        :param histogram1: List representing the first histogram (frequency values)
        :param histogram2: List representing the second histogram (frequency values)
        """
        if len(histogram1) != len(histogram2):
            raise ValueError("Histograms must have the same number of bins")
        
        HistogramIntersection.hist1 = histogram1
        HistogramIntersection.hist2 = histogram2

    @staticmethod
    def compute_intersection():
        """
        Compute the histogram intersection between the two static histograms.
        
        :return: The intersection value between two histograms
        """
        if not HistogramIntersection.hist1 or not HistogramIntersection.hist2:
            raise ValueError("Histograms are not set")

        intersection_value = 0
        for h1_bin, h2_bin in zip(HistogramIntersection.hist1, HistogramIntersection.hist2):
            intersection_value += min(h1_bin, h2_bin)

        return intersection_value

    @staticmethod
    def example():
        """
        Example usage of HistogramIntersection with two sample histograms.
        """
        hist1 = [2, 3, 5, 7, 11, 13, 17]
        hist2 = [1, 4, 5, 6, 10, 12, 15]

        # Set histograms
        HistogramIntersection.set_histograms(hist1, hist2)
        
        # Compute the intersection
        intersection_value = HistogramIntersection.compute_intersection()
        print(f"Histogram Intersection: {intersection_value}")

class EarthMoversDistance:
    def __init__(self):
        """
        Initialize the Earth Mover's Distance (EMD) calculator.
        """
        pass

    def compute_emd(self, hist1, hist2):
        """
        Compute the Earth Mover's Distance (EMD) between two histograms.
        
        :param hist1: List representing the first histogram (frequency values)
        :param hist2: List representing the second histogram (frequency values)
        :return: The Earth Mover's Distance between the two histograms
        """
        if len(hist1) != len(hist2):
            raise ValueError("Histograms must have the same number of bins")
        
        emd_value = 0
        cumulative_flow = 0

        # Calculate EMD by moving "dirt" from one bin to the next
        for i in range(len(hist1)):
            # Difference between the two histograms at the current bin + cumulative flow
            flow = hist1[i] + cumulative_flow - hist2[i]
            emd_value += abs(flow)  # Accumulate the cost
            cumulative_flow = flow  # Track the flow to the next bin

        return emd_value

    def example(self):
        """
        Example usage of Earth Mover's Distance with two sample histograms.
        """
        hist1 = [0.2, 0.5, 0.1, 0.2]
        hist2 = [0.1, 0.4, 0.3, 0.2]

        emd_value = self.compute_emd(hist1, hist2)
        print(f"Earth Mover's Distance between example histograms: {emd_value}")

class ChiSquareDistance:
    def __init__(self):
        """
        Initializes the Chi-Square Distance calculator.
        """
        pass

    def compute_chi_square(self, hist1, hist2):
        """
        Compute the Chi-Square Distance between two histograms.
        
        :param hist1: List representing the first histogram (frequency values)
        :param hist2: List representing the second histogram (frequency values)
        :return: The Chi-Square Distance between the two histograms
        """
        if len(hist1) != len(hist2):
            raise ValueError("Histograms must have the same number of bins")

        chi_square_value = 0

        for h1, h2 in zip(hist1, hist2):
            if h1 + h2 > 0:
                chi_square_value += ((h1 - h2) ** 2) / (h1 + h2)

        return chi_square_value

    def example(self):
        """
        Example usage of Chi-Square Distance with two sample histograms.
        """
        hist1 = [10, 15, 25, 30]
        hist2 = [12, 18, 22, 28]

        chi_square_value = self.compute_chi_square(hist1, hist2)
        print(f"Chi-Square Distance between example histograms: {chi_square_value}")

import cv2

class FeatureBasedDistance:
    def __init__(self, method="SIFT"):
        """
        Initialize the Feature-Based Distance calculator.
        Supported methods: SIFT, SURF, ORB.
        
        :param method: String indicating the feature detection method ("SIFT", "SURF", "ORB")
        """
        self.method = method.upper()
        
        if self.method == "SIFT":
            if cv2.__version__.startswith('3.'):
                self.detector = cv2.xfeatures2d.SIFT_create()
            else:
                self.detector = cv2.SIFT_create()
        elif self.method == "SURF":
            if cv2.__version__.startswith('3.'):
                self.detector = cv2.xfeatures2d.SURF_create()
            else:
                self.detector = cv2.SURF_create()
        elif self.method == "ORB":
            self.detector = cv2.ORB_create()
        else:
            raise ValueError("Unsupported method. Choose 'SIFT', 'SURF', or 'ORB'.")
    
    def detect_and_compute(self, image):
        """
        Detect keypoints and compute descriptors for an image.
        
        :param image: Input image (as an OpenCV image object)
        :return: Tuple of keypoints and descriptors
        """
        keypoints, descriptors = self.detector.detectAndCompute(image, None)
        return keypoints, descriptors

    def match_keypoints(self, descriptors1, descriptors2):
        """
        Match keypoints between two sets of descriptors using the BFMatcher.
        
        :param descriptors1: Descriptors from the first image
        :param descriptors2: Descriptors from the second image
        :return: List of good matches
        """
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)
        
        # Apply ratio test as per Lowe's SIFT paper
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        
        return good_matches
        
from PIL import Image
import requests
from io import BytesIO

# PerceptualHashing class (from previous implementation)
class PerceptualHashing:
    
    def __init__(self, hash_size: int = 32):
        self.hash_size: int = hash_size

    def _convert_image_to_grayscale(self, image: Image.Image) -> Image.Image:
        return image.convert("L")

    def _resize_image(self, image: Image.Image, size: int) -> Image.Image:
        return image.resize((size, size), Image.ANTIALIAS)

    def _apply_dct(self, pixels: list[list[int]]) -> list[list[float]]:
        def dct_1d(vector: list[float]) -> list[float]:
            N = len(vector)
            return [sum(vector[k] * math.cos(math.pi * n * (k + 0.5) / N) for k in range(N)) for n in range(N)]
        
        size = len(pixels)
        dct_matrix: list[list[float]] = [dct_1d(row) for row in pixels]
        return [[dct_1d([dct_matrix[k][j] for k in range(size)])[i] for j in range(size)] for i in range(size)]

    def _calculate_mean(self, pixels: list[list[float]]) -> float:
        total_sum: float = sum([sum(row) for row in pixels])
        num_pixels: int = len(pixels) * len(pixels[0]) - 1
        return (total_sum - pixels[0][0]) / num_pixels

    def _hash_from_dct(self, dct_matrix: list[list[float]]) -> str:
        mean_value: float = self._calculate_mean(dct_matrix)
        return ''.join('1' if dct_matrix[i][j] > mean_value else '0' for i in range(self.hash_size) for j in range(self.hash_size))

    def compute_hash(self, image_path: str) -> str:
        image: Image.Image = Image.open(image_path)
        gray_image: Image.Image = self._convert_image_to_grayscale(image)
        resized_image: Image.Image = self._resize_image(gray_image, self.hash_size)
        pixel_matrix: list[list[int]] = list(resized_image.getdata())
        pixel_matrix: list[list[int]] = [pixel_matrix[i * self.hash_size:(i + 1) * self.hash_size] for i in range(self.hash_size)]
        
        dct_matrix: list[list[float]] = self._apply_dct(pixel_matrix)
        binary_hash: str = self._hash_from_dct(dct_matrix)
        return '{:x}'.format(int(binary_hash, 2))

    def hamming_distance(self, hash1: str, hash2: str) -> int:
        return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

from PIL import Image
from math import sqrt

class NormalizedCrossCorrelation:
    def __init__(self):
        pass
    
    def _mean(self, data: list[list[int]]) -> float:
        total: float = sum([sum(row) for row in data])
        num_elements: int = len(data) * len(data[0])
        return total / num_elements

    def _flatten(self, data: list[list[int]]) -> list[int]:
        return [item for sublist in data for item in sublist]

    def _normalize(self, data: list[int], mean: float) -> list[float]:
        return [x - mean for x in data]

    def _dot_product(self, vec1: list[float], vec2: list[float]) -> float:
        return sum([x * y for x, y in zip(vec1, vec2)])

    def _magnitude(self, vec: list[float]) -> float:
        return sqrt(sum([x ** 2 for x in vec]))

    def compute_ncc(self, image1_path: str, image2_path: str) -> float:
        # Open images
        image1: Image.Image = Image.open(image1_path).convert('L')
        image2: Image.Image = Image.open(image2_path).convert('L')

        # Resize images to the same dimensions
        if image1.size != image2.size:
            image2 = image2.resize(image1.size)
        
        # Convert images to pixel data
        image1_data: list[list[int]] = list(image1.getdata())
        image2_data: list[list[int]] = list(image2.getdata())
        image1_data: list[list[int]] = [image1_data[i * image1.width:(i + 1) * image1.width] for i in range(image1.height)]
        image2_data: list[list[int]] = [image2_data[i * image2.width:(i + 1) * image2.width] for i in range(image2.height)]
        
        # Compute the mean of pixel intensities for each image
        mean1: float = self._mean(image1_data)
        mean2: float = self._mean(image2_data)
        
        # Flatten the pixel data
        flat_image1: list[int] = self._flatten(image1_data)
        flat_image2: list[int] = self._flatten(image2_data)
        
        # Normalize the pixel data by subtracting the mean
        norm_image1: list[float] = self._normalize(flat_image1, mean1)
        norm_image2: list[float] = self._normalize(flat_image2, mean2)
        
        # Compute the dot product and magnitudes
        numerator: float = self._dot_product(norm_image1, norm_image2)
        denominator: float = self._magnitude(norm_image1) * self._magnitude(norm_image2)
        
        # Compute NCC
        if denominator == 0:
            return 0.0  # Handle division by zero
        
        return numerator / denominator

