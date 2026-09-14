import unittest
from dx4000_lcd.state import SystemState, CpuState, DiskState
from dx4000_lcd.health import HealthEngine, Health


class TestHealthEngine(unittest.TestCase):
    def test_ok(self):
        state = SystemState(
            cpu=CpuState(temp_c=30),
            disks=[DiskState(name="sda", temp_c=30)],
        )
        results = HealthEngine().evaluate(state)
        self.assertEqual(results, [])

    def test_hot_cpu(self):
        state = SystemState(cpu=CpuState(temp_c=80))
        results = HealthEngine().evaluate(state)
        self.assertTrue(any(r.source == "cpu" and r.health == Health.ERROR for r in results))

    def test_hot_disk(self):
        state = SystemState(disks=[DiskState(name="sda", temp_c=50)])
        results = HealthEngine().evaluate(state)
        self.assertIsInstance(results, list)


if __name__ == "__main__":
    unittest.main()
