"""
# ---------------------------------------------------------------------------- #
#                           Multispectral Image Class                          #
# ---------------------------------------------------------------------------- #
"""

import cv2
import numpy as np
import tifffile


class Image:
    """
    This class is used to represent a five-band multispectral image object.

    The bands/channels of the image file should be ordered as follows:

    1. Red (R)
    2. Green (G)
    3. Blue (B)
    4. Red Edge (RE)
    5. Near Infrared (NIR)
    6. Cutline (optional)

    Parameters:
        input_path (str): Path to the .tiff file.
        cutline_included (bool): True if a cutline binary mask is included as the sixth band of the image.

    Examples:
        Loading an image from a .tiff file and accessing its shape property:

        >>> image = Image(input_path = "../data/sample/sample-image.tif")
        >>> image.shape
        (500, 500)
    """

    def __init__(self, input_path: str, cutline_included: bool = False) -> None:
        self.path = input_path
        tensor = self._load_tiff(input_path)

        self.height = tensor.shape[0]
        self.width = tensor.shape[1]
        self.shape = (self.height, self.width)

        self.red = self._correct_bands(tensor[:, :, 0])
        self.green = self._correct_bands(tensor[:, :, 1])
        self.blue = self._correct_bands(tensor[:, :, 2])
        self.rededge = self._correct_bands(tensor[:, :, 3])
        self.nir = self._correct_bands(tensor[:, :, 4])

        if cutline_included:
            self.cutline = np.uint8(
                (tensor[:, :, 5] - np.min(tensor[:, :, 5]))
                / (np.max(tensor[:, :, 5]) - np.min(tensor[:, :, 5]))
            )
            self.cutline = self.cutline.astype(bool)
        else:
            self.cutline = np.ones((self.height, self.width), dtype=bool)

    def _load_tiff(self, input_path: str) -> np.ndarray:
        """
        Load an image from a .tiff file and return it as a numpy array.

        Parameters:
            input_path (str): Path to the .tiff file.
        """
        possible_extensions = ["tiff", "tif"]
        extension = input_path.split(".")[-1]

        if extension not in possible_extensions:
            raise ValueError("Invalid file extension. Please provide a .tiff file.")

        return tifffile.imread(input_path)

    def _correct_bands(self, tensor: np.ndarray) -> np.ndarray:
        """
        Correct values in the input tensor to be within the range of 0-1.

        Parameters:
            tensor (np.ndarray): Single band of the input image.
        """
        tensor[np.where(tensor > 1)] = 1
        tensor[np.where(tensor < 0)] = 0
        return tensor

    def _normalize(
        self, tensor: np.ndarray, min_value: float = None, max_value: float = None
    ) -> np.ndarray:
        """
        Image normalization. Adapted from Micasense Image Processing
        (https://github.com/micasense/imageprocessing)

        Parameters:
            tensor (np.ndarray): Single band of the input image.
            min_value (float): Minimum value for normalization.
            max_value (float): Maximum value for normalization.

        Outputs:
            norm (np.ndarray): Normalized image.
        """
        width, height = tensor.shape
        norm = np.zeros((width, height), dtype=np.float32)

        if min_value is not None and max_value is not None:
            norm = (tensor - min_value) / (max_value - min_value)
        else:
            cv2.normalize(
                tensor,
                dst=norm,
                alpha=0.0,
                beta=1.0,
                norm_type=cv2.NORM_MINMAX,
                dtype=cv2.CV_32F,
            )
        norm[norm < 0.0] = 0.0
        norm[norm > 1.0] = 1.0
        return norm

    def _normalized_stack(self, array: np.ndarray) -> np.ndarray:
        """
        Image Stack Normalization. Adapted from Micasense Image Processing
        (https://github.com/micasense/imageprocessing)

        Parameters:
            array (np.ndarray): Multispectral image tensor.

        Outputs:
            im_display (np.ndarray): Normalized image stack
        """
        im_display = np.zeros(
            (array.shape[0], array.shape[1], array.shape[2]), dtype=np.float32
        )

        im_min = np.percentile(
            array[:, :, :].flatten(), 0.5
        )  # modify these percentiles to adjust contrast
        im_max = np.percentile(
            array[:, :, :].flatten(), 99.5
        )  # for many images, 0.5 and 99.5 are good values

        # for rgb true color, we use the same min and max scaling across the 3 bands to
        # maintain the "white balance" of the calibrated image
        for i in range(array.shape[-1]):
            im_display[:, :, i] = self._normalize(array[:, :, i], im_min, im_max)

        return im_display
    
    def get_tensor(self, cutline: bool = False):
        """
        Returns the image as a numpy array.

        Returns:
            tensor (np.ndarray): Image as a numpy array.
        """
        
        if cutline:
            tensor = np.zeros((self.height, self.width, 6), dtype=np.float32)
            tensor[:, :, 5] = self.cutline
        else:
            tensor = np.zeros((self.height, self.width, 5), dtype=np.float32)
        
        tensor[:, :, 0] = self.red
        tensor[:, :, 1] = self.green
        tensor[:, :, 2] = self.blue
        tensor[:, :, 3] = self.rededge
        tensor[:, :, 4] = self.nir

        
            
        return tensor

    def get_bgr(self):
        """
        Returns the image in normalized BGR format.

        Returns:
            bgr (np.ndarray): Image in normalized BGR format.
        """
        bgr = [self.blue, self.green, self.red]
        bgr = np.moveaxis(bgr, 0, -1)

        return self._normalized_stack(bgr)

    def get_rgb(self):
        """
        Returns the image in normalized RGB format.

        Returns:
            rgb (np.ndarray): Image in normalized RGB format.
        """
        rgb = [self.red, self.green, self.blue]
        rgb = np.moveaxis(rgb, 0, -1)

        return self._normalized_stack(rgb)

    def get_gray(self):
        """
        Returns the image in grayscale format.

        Returns:
            gray (np.ndarray): Image in grayscale format.
        """
        bgr = self.get_bgr()
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        gray = gray * 255

        return gray.astype(int)

    def get_cir(self):
        """
        Returns the image in normalized false-color (CIR) composition.

        Returns:
            cir (np.ndarray): Image in normalized CIR format.
        """
        cir = [self.nir, self.red, self.green]
        cir = np.moveaxis(cir, 0, -1)

        return self._normalized_stack(cir)

    def get_ndvi(self):
        """
        Returns the Normalized Difference Vegetation Index (NDVI).
        NDVI = (NIR - RED) / (NIR + RED)

        Returns:
            ndvi (np.ndarray): NDVI image.
        """
        with np.errstate(divide="ignore", invalid="ignore"):
            ndvi = (self.nir - self.red) / (self.nir + self.red)
            ndvi[np.isnan(ndvi)] = 0
            ndvi = np.clip(ndvi, -1, 1)
            return ndvi * (self.cutline > 0)

    def get_gndvi(self):
        """
        Returns the Green Normalized Difference Vegetation Index (GNDVI).
        GNDVI = (NIR - GREEN) / (NIR + GREEN)

        Returns:
            gndvi (np.ndarray): GNDVI image.
        """
        with np.errstate(divide="ignore", invalid="ignore"):
            gndvi = (self.nir - self.green) / (self.nir + self.green)
            gndvi[np.isnan(gndvi)] = 0
            gndvi = np.clip(gndvi, -1, 1)
            return gndvi * (self.cutline > 0)

    def get_ndre(self):
        """
        Returns the Normalized Difference Red Edge (NDRE).
        NDRE = (RE - RED) / (RE + RED)

        Returns:
            ndre (np.ndarray): NDRE image.
        """
        with np.errstate(divide="ignore", invalid="ignore"):
            ndre = (self.rededge - self.red) / (self.rededge + self.red)
            ndre[np.isnan(ndre)] = 0
            ndre = np.clip(ndre, -1, 1)
            return ndre * (self.cutline > 0)

    def get_ndwi(self):
        """
        Returns the Normalized Difference Water Index (NDWI).
        NDWI = (GREEN - NIR) / (GREEN + NIR)

        Returns:
            ndwi (np.ndarray): NDWI image.
        """
        with np.errstate(divide="ignore", invalid="ignore"):
            ndwi = (self.green - self.nir) / (self.green + self.nir)
            ndwi[np.isnan(ndwi)] = 0
            ndwi = np.clip(ndwi, -1, 1)
            return ndwi * (self.cutline > 0)
