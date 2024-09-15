import torch.nn as nn
import math


def nsd(number: int, size: int):
    """
    Next Smallest Divisible

    Finds the next smallest number that is divisible by the given size.

    :param number: The number to be adjusted to the nearest smaller divisible number.
    :param size: The divisor to which the number should be divisible.
    :returns: The largest number less than or equal to the input that is divisible by the size.
    """
    remainder = number % size
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

    before_padding_out_width = nsd(out_width, kernel_size)
    before_padding_out_height = nsd(
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
