
from hardware import (
    get_cpu_info,
    get_memory_info,
    get_storage_info,
    get_gpu_info,
)


def inspect_cpu() -> dict:
    return get_cpu_info()


def inspect_memory() -> dict:
    return get_memory_info()


def inspect_storage() -> dict:
    return get_storage_info()


def inspect_gpu() -> dict:
    return get_gpu_info()


ALL_TOOLS = [
    inspect_cpu,
    inspect_memory,
    inspect_storage,
    inspect_gpu,
]
