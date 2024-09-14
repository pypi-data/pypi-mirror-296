import torch
from .models import *
from typing import Sequence

GROUPED_CONVOLUTION = False
BATCH = 2


def from_args(runner, args):
    if len(args) > 1:
        for arg in args[1:]:
            run_on(runner, arg)
    else:
        run_on(runner)


def run_on(runner, name=None):
    if not name:
        run_all(runner)
    else:
        model_func = globals().get(name)
        if model_func:
            model, input_shape, name = model_func()
            wrapped_run(
                model, input_shape, name, runner)
        else:
            print(f'Invalid model {name}')


def check_mod(module: torch.nn.Module):
    found_conv2d = False
    grouped_conv = False
    for submodule in module.modules():
        if isinstance(submodule, torch.nn.Conv2d):
            found_conv2d = True
            if submodule.groups > 1:
                grouped_conv = True

    return grouped_conv, found_conv2d


def wrapped_run(
        module: torch.nn.Module, input_sample_shape: Sequence[int],
        name, runner):
    name = name.upper()
    print(f"{name}")
    module.eval()
    (needs_groups, has_conv) = check_mod(module)
    if needs_groups and not GROUPED_CONVOLUTION:
        print(
            f"  skipping {name} as it requires groups > 1")
    elif has_conv:
        runner(module, torch.randn(
            BATCH, *input_sample_shape), name)
    else:
        print(f"{name} doesn't use convolution")


def run_all(runner):
    wrapped_run(*alexnet(), runner)
    wrapped_run(*convnext(), runner)
    wrapped_run(*densenet(), runner)
    wrapped_run(*efficientnet(), runner)
    wrapped_run(*googlenet(), runner)
    wrapped_run(*inception(), runner)
    wrapped_run(*maxvit(), runner)
    wrapped_run(*mnasnet(), runner)
    wrapped_run(*mobilenet(), runner)
    wrapped_run(*regnet(), runner)
    wrapped_run(*resnet(), runner)
    wrapped_run(*shufflenet(), runner)
    wrapped_run(*manual_conv2d(), runner)
    wrapped_run(*squeezenet(), runner)
    wrapped_run(*swintransformer(), runner)
    wrapped_run(*vgg16(), runner)
    wrapped_run(*visiontransformer(), runner)
