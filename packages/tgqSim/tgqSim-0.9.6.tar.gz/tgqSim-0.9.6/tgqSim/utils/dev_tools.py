import logging
from subprocess import Popen, PIPE
import numpy as np
import os
import ctypes


def get_cuda_version():
    try:
        # Run nvcc command to get CUDA version
        p = Popen(["nvcc", "--version"], stdout=PIPE)
        stdout, _ = p.communicate()
        # Extract CUDA version from the output
        output = stdout.decode('utf-8')
        output_lines = output.split("\n")
        for line in output_lines:
            if line.strip().startswith("Cuda compilation tools"):
                cuda_version = line.split()[4].rstrip(",")
                return cuda_version
        return None
    except Exception as e:
        print("Error:", e)
        return None

def get_computer_cap()->str:
    """
    获取GPU卡计算能力值

    Returns:
        str: 计算能力的数值
    """
    # Run nvidia-smi command to get computer-cap
    p = Popen(["nvidia-smi",  "--query-gpu=compute_cap", "--format=csv,noheader"], stdout=PIPE)
    stdout, _ = p.communicate()
    # Extract CUDA version from the output
    computer_cap = stdout.decode('utf-8').rstrip('\n').replace('.', '')
    return computer_cap

# todo:
def get_dcu_version():
    try:
        p = Popen(["hipcc", "--version"], stdout=PIPE)
        stdout, _ = p.communicate()
        output = stdout.decode('utf-8')
        output_lines = output.split("\n")
        for line in output_lines:
            if line.strip().startswith("HIP version"):
                dcu_version = '.'.join(line.split()[-1].split('.')[:2])
                return dcu_version
        return None
    except Exception as e:
        return None


def get_computer_cap()->str:
    """
    获取GPU卡计算能力值

    Returns:
        str: 计算能力的数值
    """
    # Run nvidia-smi command to get computer-cap
    p = Popen(["nvidia-smi",  "--query-gpu=compute_cap", "--format=csv,noheader"], stdout=PIPE)
    stdout, _ = p.communicate()
    # Extract CUDA version from the output
    computer_cap = stdout.decode('utf-8').rstrip('\n').replace('.', '')
    return computer_cap


def get_normalization(frequency: dict)->dict:
    sum_freq = sum(frequency.values())
    prob = {}
    for key in frequency.keys():
        prob[key] = frequency[key] / sum_freq
    return prob


def free_state(state):
    lib = get_cuda_lib()
    lib.freeAllMem.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.complex128)
    ]
    lib.freeAllMem.restype = None
    lib.freeAllMem(state)


def get_cuda_lib():
    cuda_version = get_cuda_version().replace(".", "-")
    lib_name = f"cuda_{cuda_version}_tgq_simulator.so"
    # computer_cap = get_computer_cap()
    # lib_name = f"cuda_{cuda_version}_sm{computer_cap}_tgq_simulator.so"
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    dll_path = os.path.abspath(current_directory + '/lib/' + lib_name)
    lib = ctypes.CDLL(dll_path)
    return lib


def get_dcu_lib():
    dcu_version = get_dcu_version().replace(".", "-")
    lib_name = "dcu_{}_tgq_simulator.so".format(dcu_version,)
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    dll_path = os.path.abspath(current_directory + '/lib/' + lib_name)
    lib = ctypes.CDLL(dll_path)
    return lib


def logger():
    lg = logging.getLogger()
    lg.setLevel(logging.INFO)
    return lg

