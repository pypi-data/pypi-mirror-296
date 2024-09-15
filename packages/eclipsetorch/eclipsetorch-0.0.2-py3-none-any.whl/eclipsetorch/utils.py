import warnings
import os
import numpy as np
import torch
from PIL import Image


def tensor_to_image(tensor: torch.Tensor, batch_index: int = 0) -> Image.Image:
    """
    Converts a PyTorch tensor to a PIL image based on the number of channels.

    :param tensor: Input tensor of shape [C, H, W] or [B, C, H, W]
    :param batch_index: Index of the batch to use if the tensor has a batch dimension
    :return: PIL image created from the tensor
    """
    # Handle batch dimension
    if tensor.dim() == 4:
        tensor = tensor[batch_index]

    # Clamp values between 0 and 1 if they're not already in this range
    tensor = tensor.clamp(0, 1)

    # Convert to numpy array and scale to [0, 255] range
    tensor = (tensor * 255).byte().cpu().numpy()

    # Handle different channel configurations
    channels = tensor.shape[0]

    if channels == 1:
        # Grayscale image
        image = Image.fromarray(tensor[0], mode='L')
    elif channels == 2:
        # Grayscale with alpha channel
        image = Image.fromarray(tensor.transpose(1, 2, 0), mode='LA')
    elif channels == 3:
        # RGB image
        image = Image.fromarray(tensor.transpose(1, 2, 0), mode='RGB')
    elif channels == 4:
        # RGBA image
        image = Image.fromarray(tensor.transpose(1, 2, 0), mode='RGBA')
    else:
        # If channels > 4, use the first 4 channels (or the first 3 if less than 4)
        tensor = tensor[:4]  # Take the first 4 channels
        if tensor.shape[0] == 3:
            image = Image.fromarray(tensor.transpose(1, 2, 0), mode='RGB')
        else:
            image = Image.fromarray(tensor.transpose(1, 2, 0), mode='RGBA')

    return image


def image_to_tensor(image: Image.Image) -> torch.Tensor:
    """
    Converts a PIL image to a PyTorch tensor while preserving the image mode (RGB, RGBA).

    :param image: Input PIL image.
    :return: PyTorch tensor with shape [C, H, W], where C is determined by the image mode.
    """
    # Convert image to numpy array
    image_array = np.array(image)

    # Handle different image modes
    if image.mode == 'L':
        # Grayscale image, add channel dimension
        tensor = torch.from_numpy(image_array).unsqueeze(0)
    elif image.mode == 'LA':
        # Grayscale with alpha, keep both channels
        tensor = torch.from_numpy(image_array).permute(2, 0, 1)
    elif image.mode == 'RGB':
        # RGB image
        tensor = torch.from_numpy(image_array).permute(2, 0, 1)
    elif image.mode == 'RGBA':
        # RGBA image
        tensor = torch.from_numpy(image_array).permute(2, 0, 1)
    else:
        # Handle other modes by converting to RGBA, then to tensor
        image = image.convert('RGBA')
        tensor = torch.from_numpy(np.array(image)).permute(2, 0, 1)

    # Scale to [0, 1] range
    tensor = tensor.float() / 255.0

    return tensor


def load_image(image_path: str, convert: str = "RGB") -> Image.Image:
    """
    Loads an image from a file path and returns it as a PIL image.

    :param image_path: Path to the image file.
    :return: PIL Image object.
    """
    # Load the image using PIL
    image = Image.open(image_path).convert(
        convert)
    return image


def save_image(image: Image.Image, save_path: str):
    """
    Saves a PIL image to the specified file path.

    :param image: PIL Image object to save.
    :param save_path: Path to save the image file.
    """
    # Ensure the save directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save the image
    image.save(save_path)
    print(f"Image saved to {save_path}")


def load_images_from_folder(folder_path: str, convert: str = "RGB") -> tuple[list[Image.Image], list[str]]:
    """
    Loads all images from a specified folder and returns them as PIL images along with their absolute paths.

    :param folder_path: Path to the folder containing images.
    :param convert: Color mode to convert the images to (default is "RGB").
    :returns: A tuple containing two lists: 
              - List of PIL Image objects.
              - List of absolute paths to the loaded images.
    """
    # Supported image extensions
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

    images = []
    paths = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is an image
        if filename.lower().endswith(valid_extensions):
            image_path = os.path.join(folder_path, filename)
            try:
                # Load and convert the image
                image = Image.open(image_path).convert(convert)
                images.append(image)
                paths.append(os.path.abspath(image_path))
            except Exception as e:
                print(f"Failed to load image {image_path}: {e}")

    return images, paths


def split_batched_tensor(batched_tensor: torch.Tensor, dim: int = 0) -> list:
    """
    Splits a batched tensor into a list of individual tensors along the specified dimension.

    :param batched_tensor: A PyTorch tensor with a batch dimension.
    :param dim: The dimension along which to split the tensor (default is 0, the batch dimension).
    :return: A list of individual tensors split along the specified dimension.
    """
    # Use torch.unbind to split the tensor into individual tensors along the specified dimension
    return list(torch.unbind(batched_tensor, dim=dim))


def suppress_common_warnings():
    """
    Suppresses warnings like:
     - palette images should be RGBA images
     - you are using torch.load with weights_only = False
    """
    # Suppress the specific PIL warning
    warnings.filterwarnings("ignore",
                            message="Palette images with Transparency expressed in bytes should be converted to RGBA images"
                            )

    warnings.filterwarnings("ignore", category=FutureWarning,
                            message="You are using `torch.load` with `weights_only=False`"
                            )

    warnings.filterwarnings("ignore",
                            message=".*`huggingface_hub` cache-system uses symlinks by default.*"
                            )

    warnings.filterwarnings(
        "ignore",
        message=r".*`huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them.*"
    )
