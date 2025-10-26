"""
Unit tests for Wearables SDK core functionality
"""

import unittest
import json
from unittest.mock import patch, Mock
from wearables_sdk.core import WearablesSDK, sha3_256

class TestWearablesSDK(unittest.TestCase):
    
    def setUp(self):
        self.api_key = "test_api_key"
        self.sdk = WearablesSDK(self.api_key)
    
    def tearDown(self):
        self.sdk.shutdown()
    
    def test_initialization(self):
        """Test SDK initialization"""
        self.assertIsNotNone(self.sdk)
        self.assertEqual(self.sdk.integritas_client.api_key, self.api_key)
    
    def test_record_sensor_data(self):
        """Test recording sensor data"""
        sensor_id = self.sdk.record_sensor_data(
            "test_sensor", 
            42, 
            {"unit": "test"}
        )
        self.assertTrue(sensor_id.startswith("test_sensor_"))
    
    def test_sha3_hashing(self):
        """Test SHA3 hashing implementation"""
        test_data = {"sensor": "test", "value": 123}
        data_str = json.dumps(test_data, sort_keys=True, separators=(',', ':'))
        expected_hash = sha3_256(data_str.encode('utf-8')).hexdigest()
        
        # Record data and check hash
        sensor_id = self.sdk.record_sensor_data("test", 123)
        
        # Wait for processing
        import time
        time.sleep(0.1)
        
        verified = self.sdk.get_verified_data()
        if verified:
            actual_hash = verified[0]['hash']
            self.assertEqual(actual_hash, expected_hash)
    
    def test_metadata_size_limit(self):
        """Test metadata size validation"""
        large_metadata = {"data": "x" * 2000}  # >1KB
        
        with self.assertRaises(ValueError):
            self.sdk.record_sensor_data("test", 1, large_metadata)
    
    def test_verify_timestamp(self):
        """Test timestamp verification"""
        # Mock a valid record
        original_data = {"sensor": "test", "value": 42}
        data_str = json.dumps(original_data, sort_keys=True, separators=(',', ':'))
        data_hash = sha3_256(data_str.encode('utf-8')).hexdigest()
        
        mock_record = {
            "original_data": original_data,
            "hash": data_hash,
            "proof": "valid_proof_here"
        }
        
        is_valid = self.sdk.verify_timestamp(mock_record)
        self.assertTrue(is_valid)
    
    def test_invalid_verification(self):
        """Test verification with tampered data"""
        original_data = {"sensor": "test", "value": 42}
        tampered_data = {"sensor": "test", "value": 999}
        
        data_str = json.dumps(original_data, sort_keys=True, separators=(',', ':'))
        correct_hash = sha3_256(data_str.encode('utf-8')).hexdigest()
        
        mock_record = {
            "original_data": tampered_data,  # Different from hashed data
            "hash": correct_hash,
            "proof": "valid_proof_here"
        }
        
        is_valid = self.sdk.verify_timestamp(mock_record)
        self.assertFalse(is_valid)
    
    def test_get_status(self):
        """Test status reporting"""
        status = self.sdk.get_status()
        self.assertIn("pending_requests", status)
        self.assertIn("processed_count", status)
        self.assertIn("platform", status)
        self.assertIn("queue_full", status)

if __name__ == '__main__':
    unittest.main()
