
import os
import platform
import shutil
import subprocess
from typing import Any


def _run_read_only(command: list[str], timeout: int = 5) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def get_cpu_info() -> dict[str, Any]:
    model = "Unknown"

    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as cpu_file:
            for line in cpu_file:
                if line.lower().startswith("model name"):
                    model = line.split(":", 1)[1].strip()
                    break
                if line.lower().startswith("hardware") and model == "Unknown":
                    model = line.split(":", 1)[1].strip()

        return {
            "model": model,
            "logical_processors": os.cpu_count(),
            "architecture": platform.machine(),
        }
    except OSError as exc:
        return {"error": str(exc)}


def get_memory_info() -> dict[str, Any]:
    try:
        values = {}

        with open("/proc/meminfo", "r", encoding="utf-8") as mem_file:
            for line in mem_file:
                key, raw_value = line.split(":", 1)
                if key in {"MemTotal", "MemAvailable"}:
                    values[key] = int(raw_value.strip().split()[0])

        total_kb = values["MemTotal"]
        available_kb = values["MemAvailable"]

        return {
            "total_gb": round(total_kb / 1024 / 1024, 2),
            "available_gb": round(available_kb / 1024 / 1024, 2),
            "used_gb": round((total_kb - available_kb) / 1024 / 1024, 2),
        }
    except (OSError, ValueError, KeyError, IndexError) as exc:
        return {"error": str(exc)}


def get_storage_info() -> dict[str, Any]:
    try:
        usage = shutil.disk_usage("/")

        return {
            "mount_point": "/",
            "total_gb": round(usage.total / (1024 ** 3), 2),
            "used_gb": round(usage.used / (1024 ** 3), 2),
            "free_gb": round(usage.free / (1024 ** 3), 2),
        }
    except OSError as exc:
        return {"error": str(exc)}


def get_gpu_info() -> dict[str, Any]:
    nvidia_smi = shutil.which("nvidia-smi")

    if nvidia_smi:
        try:
            result = _run_read_only([
                nvidia_smi,
                "--query-gpu=name,memory.total,memory.used,driver_version",
                "--format=csv,noheader,nounits",
            ])

            if result.returncode == 0 and result.stdout.strip():
                devices = []

                for line in result.stdout.strip().splitlines():
                    parts = [part.strip() for part in line.split(",")]

                    if len(parts) >= 4:
                        devices.append({
                            "name": parts[0],
                            "memory_total_mb": parts[1],
                            "memory_used_mb": parts[2],
                            "driver_version": parts[3],
                        })

                if devices:
                    return {
                        "devices": devices,
                        "detection_method": "nvidia-smi",
                    }

            nvidia_error = result.stderr.strip() or "No GPU data returned"

        except (subprocess.TimeoutExpired, OSError) as exc:
            nvidia_error = str(exc)
    else:
        nvidia_error = "nvidia-smi unavailable"

    lspci = shutil.which("lspci")

    if lspci:
        try:
            result = _run_read_only([lspci])

            if result.returncode == 0:
                devices = [
                    line.strip()
                    for line in result.stdout.splitlines()
                    if any(
                        marker in line.lower()
                        for marker in ("vga", "3d controller", "display controller")
                    )
                ]

                if devices:
                    return {
                        "devices": devices,
                        "detection_method": "lspci",
                        "note": "GPU memory information is unavailable through this detection method.",
                    }

        except (subprocess.TimeoutExpired, OSError) as exc:
            lspci_error = str(exc)
        else:
            lspci_error = "No graphics devices returned"
    else:
        lspci_error = "lspci unavailable"

    return {
        "status": "unavailable",
        "message": "GPU details could not be detected from this Linux environment.",
        "nvidia_smi_status": nvidia_error,
        "lspci_status": lspci_error,
    }
