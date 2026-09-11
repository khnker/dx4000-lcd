import unittest
from dx4000_lcd.state import SystemState, CpuState, DiskState
from dx4000_lcd.renderer import HealthEngine

class TestHealthEngine(unittest.TestCase):
    def test_ok(self):
        state = SystemState(
            cpu=CpuState(temp_c=30),
            disks=[DiskState(name="sda", temp_c=30)]
        )
        self.assertEqual(HealthEngine.calculate(state), "OK")

    def test_hot_cpu(self):
        state = SystemState(cpu=CpuState(temp_c=65))
        self.assertEqual(HealthEngine.calculate(state), "HOT")

    def test_hot_disk(self):
        state = SystemState(disks=[DiskState(name="sda", temp_c=50)])
        self.assertEqual(HealthEngine.calculate(state), "HOT")

if __name__ == "__main__":
    unittest.main()
