import unittest

from hardware import (
    get_cpu_info,
    get_memory_info,
    get_storage_info,
    get_gpu_info,
    get_system_info,
)


class HardwareInspectionTests(unittest.TestCase):
    def test_cpu_returns_dictionary(self):
        result = get_cpu_info()
        self.assertIsInstance(result, dict)
        self.assertTrue(
            "model" in result or "error" in result
        )

    def test_memory_returns_dictionary(self):
        result = get_memory_info()
        self.assertIsInstance(result, dict)
        self.assertTrue(
            "total_gb" in result or "error" in result
        )

    def test_storage_returns_dictionary(self):
        result = get_storage_info()
        self.assertIsInstance(result, dict)
        self.assertTrue(
            "total_gb" in result or "error" in result
        )

    def test_gpu_returns_dictionary(self):
        result = get_gpu_info()
        self.assertIsInstance(result, dict)

    def test_system_returns_dictionary(self):
        result = get_system_info()
        self.assertIsInstance(result, dict)
        self.assertIn("is_wsl", result)


if __name__ == "__main__":
    unittest.main()
