import torch
import torchvision.models as m
from torch import nn
from torch.nn.utils import spectral_norm, weight_norm


def noop(x):
    return x


def init_cnn(m):
    """
    Initialize a cnn with kaiming_normal_ or constant
    """
    if getattr(m, "bias", None) is not None:
        nn.init.constant_(m.bias, 0)
    if isinstance(m, (nn.Conv2d, nn.Linear)):
        nn.init.kaiming_normal_(m.weight)
    for l in m.children():
        init_cnn(l)


class Flatten(nn.Module):
    """
    Flatten
    """

    def forward(self, x):
        return x.view(x.size(0), -1)
