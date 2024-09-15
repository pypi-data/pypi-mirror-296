import torch
import torch.nn as nn
import math
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


def next_smallest_divisible(number, N):
    remainder = number % N
    if remainder == 0:
        return number
    return number - remainder


def conv(in_channels, out_channels, in_width, in_height, out_width, out_height, kernel_size: int = 3):
    """
    Replaces the functionality of unconv using Conv2d layers instead of ConvTranspose2d.

    :param in_channels: Number of input channels
    :param out_channels: Number of output channels
    :param in_width: Initial width of the input
    :param in_height: Initial height of the input
    :param out_width: Desired output width
    :param out_height: Desired output height
    :param kernel_size: Size of the convolutional kernel
    :returns: List of layers that replicate the behavior of unconv using Conv2d
    """

    # Ensure the kernel size is not larger than the output width or height
    if kernel_size > out_width:
        kernel_size = out_width
    if kernel_size > out_height:
        kernel_size = out_height

    desired_in_width = out_width * kernel_size
    desired_in_height = out_height * kernel_size

    layers = []

    if in_width != desired_in_width or in_height != desired_in_height:
        resize = nn.Upsample(size=(desired_in_width, desired_in_height),
                             mode='bilinear', align_corners=True)
        layers.append(resize)

    main_conv = nn.Conv2d(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=(kernel_size, kernel_size),
        stride=(kernel_size, kernel_size)
    )
    layers.append(main_conv)

    return layers


def unconv(in_channels, out_channels, in_width, in_height, out_width, out_height, kernel_size: int = 3):
    """
    Creates a sequence of layers that upsample an input tensor to a specified output size using ConvTranspose2d.

    This function adjusts the input tensor dimensions through upsampling, transposed convolution, and padding to match 
    the desired output size. It calculates the necessary padding and scaling factors to achieve the exact output width 
    and height specified. The transposed convolution layer is used to perform the upsampling operation, which expands 
    the spatial dimensions of the input.

    :param in_channels: Number of input channels
    :param out_channels: Number of output channels
    :param in_width: Initial width of the input tensor
    :param in_height: Initial height of the input tensor
    :param out_width: Desired width of the output tensor
    :param out_height: Desired height of the output tensor
    :param kernel_size: Size of the convolutional kernel (default is 3)
    :returns: A list of layers to be used in nn.Sequential, including Upsample, ConvTranspose2d, and ReplicationPad2d
    """

    # make sure kernel size is not larger than out widht or height
    if kernel_size > out_width:
        kernel_size = out_width
    if kernel_size > out_height:
        kernel_size = out_height

    before_padding_out_width = next_smallest_divisible(out_width, kernel_size)
    before_padding_out_height = next_smallest_divisible(
        out_height, kernel_size)

    after_padding_out_x = out_width - before_padding_out_width
    after_padding_out_y = out_height - before_padding_out_height

    first_after_padding_out_x = math.ceil(after_padding_out_x / 2)
    second_after_padding_out_x = math.floor(after_padding_out_x / 2)
    first_after_padding_out_y = math.ceil(after_padding_out_y / 2)
    second_after_padding_out_y = math.floor(after_padding_out_y / 2)

    desired_in_width = int(before_padding_out_width / kernel_size)
    desired_in_height = int(before_padding_out_height / kernel_size)

    layers = []

    if desired_in_width != in_width or desired_in_height != in_height:
        upsample = nn.Upsample(
            size=(desired_in_height, desired_in_width), mode='bilinear', align_corners=True)
        layers.append(upsample)

    main_conv = nn.ConvTranspose2d(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=(kernel_size, kernel_size),
        stride=(kernel_size, kernel_size),
    )
    layers.append(main_conv)

    if first_after_padding_out_x != 0 or second_after_padding_out_x != 0 or first_after_padding_out_y != 0 or second_after_padding_out_y != 0:
        after_padding = nn.ReplicationPad2d(
            (first_after_padding_out_x, second_after_padding_out_x, first_after_padding_out_y, second_after_padding_out_y))
        layers.append(after_padding)

    return layers
