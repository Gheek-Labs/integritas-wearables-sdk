"""
Integration tests for example implementations
"""

import unittest
import sys
import os

# Add examples directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))

class TestExamples(unittest.TestCase):
    
    def test_health_monitoring_import(self):
        """Test that health monitoring example can be imported"""
        try:
            import health_monitoring
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Could not import health_monitoring: {e}")
    
    def test_fitness_tracking_import(self):
        """Test that fitness tracking example can be imported"""
        try:
            import fitness_tracking
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Could not import fitness_tracking: {e}")
    
    def test_environmental_sensing_import(self):
        """Test that environmental sensing example can be imported"""
        try:
            import environmental_sensing
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Could not import environmental_sensing: {e}")

if __name__ == '__main__':
    unittest.main()
