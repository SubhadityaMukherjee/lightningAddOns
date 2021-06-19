import os
import random

import matplotlib.pyplot as plt
import numpy as np
import PIL
import torch
import torchvision
from prettytable import PrettyTable
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


def clear_memory():
    """
    Clear GPU cache
    """
    torch.cuda.empty_cache()


def seed_everything(seed=42):
    """
    Seed everything with a number
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class FreezeUnfreeze:
    def __init__(self, model, switch, to=None):
        self.model = model
        self.switch = switch  # 0 for freeze, 1 for unfreeze
        self.ps = [None for x in self.model.parameters()]
        self.count = 0
        self.to = to

    def runner(self):
        if self.to == None:
            self.to = len(self.ps)
        if self.to < 0:
            self.to = len(self.ps) - abs(self.to)
        for param in self.model.parameters():
            if self.count < self.to:
                param.requires_grad = False if self.switch == 0 else True
                self.count += 1


def freeze_to(model, to=None):
    FreezeUnfreeze(model, 0, to).runner()


def unfreeze_to(model, to=None):
    FreezeUnfreeze(model, 1, to).runner()


def count_parameters(model, show_table=False):
    table = PrettyTable(["Modules", "Parameters"])
    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        param = parameter.numel()
        table.add_row([name, param])
        total_params += param

    print(f"Total Trainable Params: {total_params}")
    if show_table == True:
        print(table)
    return total_params


def param_state(x):
    return x.requires_grad


def total_layer_state(learn):
    ps = [param_state(x) for x in learn.model.parameters()]
    frozen = ps.count(False)
    return f"Frozen: {frozen}, Not: {len(ps)-frozen}, Total: {len(ps)}"


def open_image(fpath, size, convert_to="", to_tensor=False, perm=()):
    tem = PIL.Image.open(fpath).resize(size)
    if len(convert_to) > 1:
        tem = tem.convert(convert_to)
    if to_tensor == True:
        tem = pil_to_tensor(tem)
    if len(perm) > 2:
        tem = tem.permute(*perm)

    return tem


def pil_from_tensor(x):
    return torchvision.transforms.functional.to_pil_image(x)


def pil_to_tensor(x):
    return torchvision.transforms.functional.to_tensor(x)
