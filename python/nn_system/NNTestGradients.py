from __future__ import print_function, absolute_import

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
torch.manual_seed(1)

import pydrake
import pydrake.autodiffutils
from pydrake.autodiffutils import AutoDiffXd
from pydrake.systems.framework import (
    AbstractValue,
    BasicVector, BasicVector_
)

from NNSystem import NNSystem, NNSystem_
from NNTestSetup import NNTestSetup
from NNSystemHelper import FC, MLP

# nn_test_setup = NNTestSetup(pytorch_nn_object=MLP())
# nn_test_setup.RunSimulation()

# Define network, input
torch.set_default_tensor_type('torch.DoubleTensor')
net = FC()
net = MLP()
autodiff_in = np.array([
    [AutoDiffXd(1.0, [1.0, 0.0]),],        
    [AutoDiffXd(1.0, [1.0, 0.0]),]
])

# Make system and give input
nn_system = NNSystem_[AutoDiffXd](pytorch_nn_object=net)
context = nn_system.CreateDefaultContext()
context.FixInputPort(0, autodiff_in)

# Allocate and Eval output
output = nn_system.AllocateOutput()
nn_system.CalcOutput(context, output)
autodiff = output.get_vector_data(0).CopyToVector()[0]
print("autodiff: ", autodiff)
print("derivatives: ", autodiff.derivatives())

