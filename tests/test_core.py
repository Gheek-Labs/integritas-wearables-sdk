import unittest, json, time
from wearables_sdk.core import WearablesSDK, sha3_256

class TestCore(unittest.TestCase):
    def test_metadata_limit(self):
        sdk = WearablesSDK("dummy")
        try:
            with self.assertRaises(ValueError):
                sdk.record_sensor_data("x", 1, {"data": "x"*2000})
        finally:
            sdk.shutdown()

if __name__ == "__main__":
    unittest.main()
