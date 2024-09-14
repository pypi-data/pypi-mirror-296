import os
import platform

import sys
current_module = sys.modules[__name__]

# import torch to load in directml
import torch
from torch.storage import _StorageBase
from torch._C import default_generator

# Load the directml dll into the process
platform = 'win' if platform.system() == 'Windows' else 'linux'
if platform == 'win':
    directml_dll = os.path.join(os.path.dirname(__file__), 'DirectML.dll')
else:
    directml_dll = os.path.join(os.path.dirname(__file__), 'libdirectml.so')
torch.ops.load_library(directml_dll)

# import native apis
import torch_directml_native

from .device import *
from .functions import *

# # Register backend to support AMP
class PrivateUse1Module:
    @staticmethod
    def is_available() -> bool:
        r"""Returns a bool indicating if DML is currently available."""
        if not hasattr(torch_directml_native, 'get_device_count'):
            return False
        # This function never throws and returns 0 if driver is missing or can't
        # be initialized
        return torch_directml_native.get_device_count() > 0

    @staticmethod
    def device_count() -> int:
        r"""Returns the number of GPUs available."""
        if is_available():
            return torch_directml_native.get_device_count()
        else:
            return 0

    @staticmethod
    def device_name(device_id) -> str:
        r"""Returns the device name of the specified index."""
        if device_id >= 0 and device_id < device_count():
            return torch_directml_native.get_device_name(device_id)
        else:
            return ""

    @staticmethod
    def default_device() -> int:
        r"""Returns the index of the default selected device."""
        return torch_directml_native.get_default_device()

    @staticmethod
    def device(device_id = None) -> str:
        r"""Returns the torch device at the specified index."""
        num_devices = device_count()
        if device_id is None:
            return torch_directml_native.custom_device(default_device())
        elif device_id >= 0 and device_id < num_devices:
            return torch_directml_native.custom_device(device_id)
        else:
            raise Exception(f"Invalid device_id argument supplied {device_id}. device_id must be in range [0, {num_devices}).")

    @staticmethod
    def disable_tiled_resources(is_disabled):
        torch_directml_native.disable_tiled_resources(is_disabled)

    @staticmethod
    def has_float64_support(device_id = default_device()):
        return torch_directml_native.has_float64_support(device_id)

    @staticmethod
    def gpu_memory(device_id = default_device(), mb_per_tile = 1):
        return torch_directml_native.get_gpu_memory(device_id, mb_per_tile)

    @staticmethod
    def is_autocast_enabled():
        return False

    @staticmethod
    def get_autocast_dtype():
        return torch.float16

    @staticmethod
    def set_autocast_enabled(enable):
        pass

    @staticmethod
    def set_autocast_dtype(dtype):
        pass

    @staticmethod
    def get_amp_supported_dtype():
        return [torch.float16]
    
    @staticmethod
    def _is_in_bad_fork():
        return False
    
    @staticmethod
    def manual_seed_all(seed: int) -> None:
        # We use the CPU Generator for the random number generation
        default_generator.manual_seed(seed)

    # Returns a copy of the given object in dml memory
    # Contiguous, one-dimensional array of elements of a
    # particular torch.dtype. It can be given any torch.dtype,
    # and the internal data will be interpreted appropriately.
    # torch.TypedStorage contains a torch.UntypedStorage which
    # holds the data as an untyped array of bytes.
    def _dml(self, dev=None, non_blocking=False, **kwargs):
        """Returns a copy of this object in dml memory.

            If this object is already in dml memory and on the correct device, then
            no copy is performed and the original object is returned.

            Args:
                dev (int): The destination GPU id. Defaults to the current device.
                non_blocking (bool): If ``True`` and the source is in pinned memory,
                    the copy will be asynchronous with respect to the host. Otherwise,
                    the argument has no effect.
        """
        non_blocking = torch._utils._get_async_or_non_blocking("privateuseone", non_blocking, kwargs)
        if dev is None:
            dml_device = device(default_device())
        else:
            dml_device = device(dev)

        with dml_device:
            if self.is_sparse:
                raise RuntimeError("UntypedStorage sparse copy is not supported.")
            else:
                untyped_storage = torch.UntypedStorage(self.size())
                untyped_storage.copy_(self, non_blocking)
                return untyped_storage

_StorageBase.privateuseone = PrivateUse1Module._dml
torch._register_device_module('privateuseone', PrivateUse1Module)
