# wearables_sdk/core.py
import json
import time
import threading
import queue
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import sys

# Platform detection
IS_ANDROID = 'android' in sys.platform.lower()
IS_IOS = sys.platform == 'darwin' and hasattr(sys, 'getandroidapilevel') == False
IS_TIZEN = 'tizen' in sys.platform.lower()

# Conditional imports for SHA3
try:
    import hashlib
    sha3_256 = hashlib.sha3_256
except AttributeError:
    try:
        from sha3 import sha3_256
    except ImportError:
        raise ImportError("SHA3 support required. Install with: pip install pysha3")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TimestampResponse:
    """Response structure from Integritas API"""
    success: bool
    timestamp: Optional[str] = None
    hash: Optional[str] = None
    proof: Optional[str] = None
    error: Optional[str] = None

class IntegritasClient:
    """Handles communication with Integritas Minima Global API"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.integritas.minima.global"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"WearablesSDK/1.0 ({sys.platform})"
        })
    
    def timestamp_data(self, data_hash: str) -> TimestampResponse:
        """Send SHA3 hash to Integritas for timestamping"""
        try:
            response = self.session.post(
                f"{self.base_url}/v1/timestamp",
                json={"hash": data_hash},
                timeout=(5, 10)
            )
            response.raise_for_status()
            data = response.json()
            
            return TimestampResponse(
                success=True,
                timestamp=data.get("timestamp"),
                hash=data.get("hash"),
                proof=data.get("proof")
            )
        except Exception as e:
            logger.error(f"Timestamp request failed: {str(e)}")
            return TimestampResponse(success=False, error=str(e))

class WearableDataProcessor:
    """Processes wearable sensor data with SHA3 hashing"""
    
    def __init__(self, integritas_client: IntegritasClient):
        self.client = integritas_client
        self.pending_queue = queue.Queue(maxsize=100)
        self.processed_data = []
        self._worker_thread = None
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
    
    def start_background_processing(self):
        """Start background thread"""
        if self._worker_thread is None:
            self._worker_thread = threading.Thread(target=self._process_queue, name="TimestampWorker")
            self._worker_thread.daemon = True
            self._worker_thread.start()
    
    def stop_background_processing(self):
        """Stop background processing"""
        self._stop_event.set()
        if self._worker_thread:
            try:
                self.pending_queue.put_nowait(None)
            except queue.Full:
                pass
            self._worker_thread.join(timeout=2.0)
    
    def _process_queue(self):
        """Background worker"""
        while not self._stop_event.is_set():
            try:
                item = self.pending_queue.get(timeout=1)
                if item is None:
                    break
                
                result = self.client.timestamp_data(item['hash'])
                with self._lock:
                    if result.success:
                        item['timestamp'] = result.timestamp
                        item['proof'] = result.proof
                        self.processed_data.append(item)
                        logger.info(f"Timestamped: {item['id']}")
                    else:
                        logger.error(f"Failed {item['id']}: {result.error}")
                        if item.get('retry_count', 0) < 2:
                            item['retry_count'] = item.get('retry_count', 0) + 1
                            try:
                                self.pending_queue.put_nowait(item)
                            except queue.Full:
                                logger.warning("Queue full, dropping retry")
                
                self.pending_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.exception(f"Queue processing error: {e}")
    
    def add_sensor_reading(self, sensor_type: str, value: Any, metadata: Dict = None) -> str:
        """Add sensor reading with SHA3-256 hashing"""
        reading_id = f"{sensor_type}_{int(time.time() * 1000)}"
        data_dict = {
            "id": reading_id,
            "sensor_type": sensor_type,
            "value": value,
            "timestamp_request": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        data_str = json.dumps(data_dict, sort_keys=True, separators=(',', ':'))
        data_hash = sha3_256(data_str.encode('utf-8')).hexdigest()
        
        queue_item = {
            "id": reading_id,
            "hash": data_hash,
            "original_data": data_dict
        }
        
        try:
            self.pending_queue.put_nowait(queue_item)
        except queue.Full:
            logger.error("Queue full, dropping sensor reading")
            raise RuntimeError("Timestamp queue full - data dropped")
        
        return reading_id
    
    def get_processed_data(self) -> List[Dict]:
        """Thread-safe access to processed data"""
        with self._lock:
            return self.processed_data.copy()
    
    def get_pending_count(self) -> int:
        """Get current queue size"""
        return self.pending_queue.qsize()

class WearablesSDK:
    """Main SDK interface optimized for wearable platforms"""
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
            
        self.integritas_client = IntegritasClient(api_key)
        self.data_processor = WearableDataProcessor(self.integritas_client)
        self.data_processor.start_background_processing()
    
    def record_sensor_data(self, sensor_type: str, value: Any, metadata: Dict = None) -> str:
        if metadata and len(json.dumps(metadata)) > 1024:
            raise ValueError("Metadata too large (>1KB)")
        return self.data_processor.add_sensor_reading(sensor_type, value, metadata)
    
    def get_verified_data(self) -> List[Dict]:
        return self.data_processor.get_processed_data()
    
    def verify_timestamp(self, data_record: Dict) -> bool:
        if not data_record.get('proof'):
            return False
            
        original = data_record['original_data']
        data_str = json.dumps(original, sort_keys=True, separators=(',', ':'))
        recalculated_hash = sha3_256(data_str.encode('utf-8')).hexdigest()
        return recalculated_hash == data_record['hash']
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "pending_requests": self.data_processor.get_pending_count(),
            "processed_count": len(self.data_processor.processed_data),
            "platform": sys.platform,
            "queue_full": self.data_processor.pending_queue.full()
        }
    
    def shutdown(self):
        self.data_processor.stop_background_processing()
