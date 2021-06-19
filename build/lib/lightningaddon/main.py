import torch
from torch import nn

def flatten(x):
    """
    Flatten tensor
    """
    return x.view(x.shape[0], -1)


def get_hist(h):
    """
    grab histogram
    """
    return torch.stack(h.stats[2]).t().float().log1p()


def get_min(h):
    """
    Grab min values from histogram
    """
    h1 = torch.stack(h.stats[2]).t().float()
    return h1[19:22].sum(0) / h1.sum(0)

def find_modules(m, cond):
    """
    Return modules with a condition
    """
    if cond(m):
        return [m]
    return sum([find_modules(o, cond) for o in m.children()], [])


def is_lin_layer(l):
    """
    Check if linear
    """
    lin_layers = (nn.Conv1d, nn.Conv2d, nn.Conv3d, nn.Linear, nn.ReLU)
    return isinstance(l, lin_layers)


