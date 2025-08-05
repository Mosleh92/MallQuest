#!/usr/bin/env python3
"""
Performance Module for Deerfields Mall Gamification System
Provides comprehensive performance optimizations including caching, async processing,
memory-efficient effects management, and performance monitoring.
"""

import time
import threading
import sqlite3
import asyncio
from collections import deque
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional
import logging
import json

# Optional Redis import
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("[⚠️] Redis not available - using memory-based caching")

# Optional psutil import for performance monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("[⚠️] psutil not available - limited performance monitoring")

class PerformanceManager:
    """Manages Redis client for caching and performance optimization"""
    
    def __init__(self):
        self.redis_client = None
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.setup_redis()
    
    def setup_redis(self):
        """Setup Redis for caching"""
        if not REDIS_AVAILABLE:
            print("[⚠️] Redis not available - using memory-based caching")
            return
            
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
            self.redis_client.ping()
            print("[✅] Redis connected successfully")
        except Exception as e:
            print(f"[⚠️] Redis not available: {e}")
            self.redis_client = None
    
    def get_cache(self, key: str) -> Optional[str]:
        """Get value from Redis cache"""
        if self.redis_client:
            try:
                return self.redis_client.get(key)
            except Exception as e:
                print(f"[⚠️] Redis get error: {e}")
        return None
    
    def set_cache(self, key: str, value: str, ttl: int = 300) -> bool:
        """Set value in Redis cache with TTL"""
        if self.redis_client:
            try:
                self.redis_client.setex(key, ttl, value)
                return True
            except Exception as e:
                print(f"[⚠️] Redis set error: {e}")
        return False
    
    def clear_cache(self, pattern: str = "*") -> bool:
        """Clear cache entries matching pattern"""
        if self.redis_client:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
                return True
            except Exception as e:
                print(f"[⚠️] Redis clear error: {e}")
        return False

class MemoryEfficientEffects:
    """Memory-efficient effects manager with automatic cleanup"""
    
    def __init__(self, max_effects: int = 100):
        self.active_effects = deque(maxlen=max_effects)
        self.effect_cleanup_thread = None
        self.running = True
        self.start_cleanup_thread()
    
    def add_effect(self, effect: dict):
        """Add effect with automatic expiration"""
        effect['created_at'] = time.time()
        effect['expires_at'] = time.time() + effect.get('duration', 3.0)
        self.active_effects.append(effect)
    
    def start_cleanup_thread(self):
        """Start background thread for effect cleanup"""
        def cleanup_loop():
            while self.running:
                try:
                    self.cleanup_expired_effects()
                    time.sleep(1.0)  # Check every second
                except Exception as e:
                    print(f"[⚠️] Effect cleanup error: {e}")
                    time.sleep(5.0)  # Wait longer on error
        
        self.effect_cleanup_thread = threading.Thread(
            target=cleanup_loop, 
            daemon=True
        )
        self.effect_cleanup_thread.start()
    
    def cleanup_expired_effects(self):
        """Remove expired effects"""
        current_time = time.time()
        # Convert to list to avoid modification during iteration
        effects_to_remove = []
        
        for i, effect in enumerate(self.active_effects):
            if effect.get('expires_at', 0) < current_time:
                effects_to_remove.append(i)
        
        # Remove from right to left to maintain indices
        for i in reversed(effects_to_remove):
            if i < len(self.active_effects):
                del self.active_effects[i]
    
    def get_active_effects(self) -> List[dict]:
        """Get list of active effects"""
        return list(self.active_effects)
    
    def stop_cleanup(self):
        """Stop the cleanup thread"""
        self.running = False
        if self.effect_cleanup_thread:
            self.effect_cleanup_thread.join(timeout=5.0)

class CachedDatabase:
    """Database with intelligent caching"""
    
    def __init__(self, db_path: str = 'mall_gamification.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.user_cache = {}
        self.cache_ttl = 300  # 5 minutes
        self.performance_manager = PerformanceManager()
        self.logger = logging.getLogger(__name__)
    
    @lru_cache(maxsize=1000)
    def get_user_cached(self, user_id: str, cache_time: int):
        """Get user with LRU cache (cache_time for cache invalidation)"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM users WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Database error: {e}")
            return None
    
    def get_user(self, user_id: str):
        """Get user with time-based cache invalidation"""
        current_time = int(time.time())
        cache_window = current_time // self.cache_ttl
        return self.get_user_cached(user_id, cache_window)
    
    def batch_update_users(self, user_updates: List[tuple]) -> bool:
        """Batch update multiple users for better performance"""
        if not user_updates:
            return True
        
        try:
            # Begin transaction
            self.conn.execute('BEGIN TRANSACTION')
            
            for user_id, updates in user_updates:
                if updates:
                    set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
                    set_clause += ', updated_at = CURRENT_TIMESTAMP'
                    
                    query = f"UPDATE users SET {set_clause} WHERE user_id = ?"
                    params = tuple(updates.values()) + (user_id,)
                    self.conn.execute(query, params)
            
            self.conn.commit()
            
            # Invalidate cache for updated users
            for user_id, _ in user_updates:
                self.get_user_cached.cache_clear()
            
            return True
            
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"Batch update error: {e}")
            return False
    
    def execute_safe_query(self, query: str, params: tuple = ()):
        """Execute parameterized query safely"""
        try:
            cursor = self.conn.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            self.conn.rollback()
            self.logger.error(f"Database error: {e}")
            raise

class AsyncTaskManager:
    """Async task manager for non-blocking operations"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.logger = logging.getLogger(__name__)
    
    async def process_receipt_async(self, user_id: str, amount: float, store: str):
        """Process receipt asynchronously"""
        loop = asyncio.get_event_loop()
        
        # Run CPU-intensive tasks in thread pool
        result = await loop.run_in_executor(
            self.executor,
            self._process_receipt_sync,
            user_id, amount, store
        )
        
        return result
    
    def _process_receipt_sync(self, user_id: str, amount: float, store: str):
        """Synchronous receipt processing"""
        # AI verification (CPU intensive)
        verification = self._ai_verify_receipt(amount, store)
        
        if verification['valid']:
            coins_earned = int(amount // 10)
            # Database update
            return {
                'status': 'success',
                'coins_earned': coins_earned
            }
        else:
            return {
                'status': 'rejected',
                'reason': verification['reason']
            }
    
    def _ai_verify_receipt(self, amount: float, store: str) -> dict:
        """Simulate AI verification (replace with actual AI)"""
        # Simulate processing time
        time.sleep(0.1)
        
        if store.lower().startswith("deerfields") and amount > 0:
            return {'valid': True, 'confidence': 0.95}
        else:
            return {'valid': False, 'reason': 'invalid_store', 'confidence': 0.8}
    
    def shutdown(self):
        """Shutdown the thread pool"""
        self.executor.shutdown(wait=True)

class OptimizedGraphicsEngine:
    """Optimized graphics engine with better resource management"""
    
    def __init__(self):
        self.effects_manager = MemoryEfficientEffects(max_effects=50)
        self.render_queue = deque(maxlen=100)
        self.last_render_time = 0
        self.target_fps = 60
        self.frame_time = 1.0 / self.target_fps
        self.logger = logging.getLogger(__name__)
    
    def trigger_effect(self, effect_type: str, **kwargs):
        """Trigger effect with performance considerations"""
        # Limit effect frequency
        current_time = time.time()
        if current_time - self.last_render_time < self.frame_time:
            return {"status": "throttled", "message": "Effect rate limited"}
        
        effect = {
            "type": effect_type,
            "duration": kwargs.get("duration", 2.0),
            "data": kwargs
        }
        
        self.effects_manager.add_effect(effect)
        self.last_render_time = current_time
        
        return {"status": "success", "effect": effect}
    
    def render_frame(self):
        """Render frame with performance monitoring"""
        start_time = time.time()
        
        # Process render queue
        active_effects = list(self.effects_manager.active_effects)
        
        # Simulate rendering
        for effect in active_effects:
            self._render_effect(effect)
        
        render_time = time.time() - start_time
        
        # Performance logging
        if render_time > self.frame_time:
            self.logger.warning(f"Frame time exceeded: {render_time:.3f}s")
        
        return {
            "effects_rendered": len(active_effects),
            "render_time": render_time,
            "fps": 1.0 / render_time if render_time > 0 else 0
        }
    
    def _render_effect(self, effect: dict):
        """Render individual effect"""
        # Simulate effect rendering
        pass
    
    def shutdown(self):
        """Shutdown the graphics engine"""
        self.effects_manager.stop_cleanup()

class PerformanceMonitor:
    """Tracks and reports performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'requests_per_second': 0,
            'average_response_time': 0,
            'memory_usage': 0,
            'active_effects': 0
        }
        self.request_times = deque(maxlen=100)
        self.logger = logging.getLogger(__name__)
    
    def record_request(self, response_time: float):
        """Record request for performance monitoring"""
        self.request_times.append(response_time)
        
        # Update metrics
        if self.request_times:
            self.metrics['average_response_time'] = sum(self.request_times) / len(self.request_times)
            self.metrics['requests_per_second'] = len(self.request_times) / 60  # Approximate RPS
    
    def get_performance_report(self) -> dict:
        """Get performance report"""
        if PSUTIL_AVAILABLE:
            try:
                self.metrics['memory_usage'] = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            except Exception as e:
                self.logger.error(f"Error getting memory usage: {e}")
        else:
            self.metrics['memory_usage'] = 0
        
        return self.metrics.copy()
    
    def log_performance_metrics(self):
        """Log current performance metrics"""
        report = self.get_performance_report()
        self.logger.info(f"Performance Report: {report}")

# Global instances
performance_manager = PerformanceManager()
performance_monitor = PerformanceMonitor()
optimized_graphics = OptimizedGraphicsEngine()

# Convenience functions
def get_performance_manager() -> PerformanceManager:
    """Get global performance manager instance"""
    return performance_manager

def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance"""
    return performance_monitor

def get_optimized_graphics() -> OptimizedGraphicsEngine:
    """Get global optimized graphics engine instance"""
    return optimized_graphics

def record_performance_event(event_type: str, duration: float = None):
    """Record a performance event"""
    if duration:
        performance_monitor.record_request(duration)
    
    performance_monitor.logger.info(f"Performance Event: {event_type}")

def cleanup_performance_resources():
    """Cleanup all performance-related resources"""
    try:
        optimized_graphics.shutdown()
        performance_manager.thread_pool.shutdown(wait=True)
        print("[✅] Performance resources cleaned up")
    except Exception as e:
        print(f"[⚠️] Error cleaning up performance resources: {e}")

class SmartCacheManager:
    """
    Smart Cache Manager to address unlimited memory growth
    Implements LRU cache with Redis fallback and automatic cleanup
    """
    
    def __init__(self, memory_limit: int = 1000, redis_ttl: int = 3600):
        self.memory_limit = memory_limit
        self.redis_ttl = redis_ttl
        self.redis_client = None
        self._cache = {}
        self._access_order = deque(maxlen=memory_limit)
        self._setup_redis()
        self.logger = logging.getLogger(__name__)
    
    def _setup_redis(self):
        """Setup Redis connection for persistent caching"""
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.Redis(host='localhost', port=6379, db=1)
                self.redis_client.ping()
                print("[✅] SmartCacheManager: Redis connected")
            except Exception as e:
                print(f"[⚠️] SmartCacheManager: Redis not available: {e}")
                self.redis_client = None
    
    def get_user_data(self, user_id: str) -> Optional[dict]:
        """Get user data with smart caching strategy"""
        # First check memory cache
        if user_id in self._cache:
            self._update_access_order(user_id)
            return self._cache[user_id]
        
        # Then check Redis
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(f"user:{user_id}")
                if cached_data:
                    user_data = json.loads(cached_data)
                    self._add_to_memory_cache(user_id, user_data)
                    return user_data
            except Exception as e:
                self.logger.error(f"Redis get error: {e}")
        
        # Finally fetch from database
        user_data = self._fetch_from_database(user_id)
        if user_data:
            self._add_to_memory_cache(user_id, user_data)
            self._add_to_redis_cache(user_id, user_data)
        
        return user_data
    
    def get_store_data(self, store_id: str) -> Optional[dict]:
        """Get store data with smart caching strategy"""
        # First check memory cache
        if store_id in self._cache:
            self._update_access_order(store_id)
            return self._cache[store_id]
        
        # Then check Redis
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(f"store:{store_id}")
                if cached_data:
                    store_data = json.loads(cached_data)
                    self._add_to_memory_cache(store_id, store_data)
                    return store_data
            except Exception as e:
                self.logger.error(f"Redis get error: {e}")
        
        # Finally fetch from database
        store_data = self._fetch_store_from_database(store_id)
        if store_data:
            self._add_to_memory_cache(store_id, store_data)
            self._add_to_redis_cache(store_id, store_data)
        
        return store_data
    
    def set_user_data(self, user_id: str, user_data: dict) -> bool:
        """Set user data with smart caching"""
        try:
            # Update memory cache
            self._add_to_memory_cache(user_id, user_data)
            
            # Update Redis cache
            self._add_to_redis_cache(user_id, user_data)
            
            # Update database
            self._update_database_user(user_id, user_data)
            
            return True
        except Exception as e:
            self.logger.error(f"Error setting user data: {e}")
            return False
    
    def set_store_data(self, store_id: str, store_data: dict) -> bool:
        """Set store data with smart caching"""
        try:
            # Update memory cache
            self._add_to_memory_cache(store_id, store_data)
            
            # Update Redis cache
            self._add_to_redis_cache(store_id, store_data)
            
            # Update database
            self._update_database_store(store_id, store_data)
            
            return True
        except Exception as e:
            self.logger.error(f"Error setting store data: {e}")
            return False
    
    def _add_to_memory_cache(self, key: str, data: dict):
        """Add data to memory cache with LRU eviction"""
        # If cache is full, remove least recently used item
        if len(self._cache) >= self.memory_limit:
            if self._access_order:
                lru_key = self._access_order.popleft()
                if lru_key in self._cache:
                    del self._cache[lru_key]
        
        # Add new data
        self._cache[key] = data
        self._access_order.append(key)
    
    def _add_to_redis_cache(self, key: str, data: dict):
        """Add data to Redis cache"""
        if self.redis_client:
            try:
                cache_key = f"user:{key}" if "coins" in data else f"store:{key}"
                self.redis_client.setex(
                    cache_key, 
                    self.redis_ttl, 
                    json.dumps(data)
                )
            except Exception as e:
                self.logger.error(f"Redis set error: {e}")
    
    def _update_access_order(self, key: str):
        """Update access order for LRU tracking"""
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
    
    def _fetch_from_database(self, user_id: str) -> Optional[dict]:
        """Fetch user data from database"""
        try:
            # This would connect to the actual database
            # For now, return None to simulate database miss
            return None
        except Exception as e:
            self.logger.error(f"Database fetch error: {e}")
            return None
    
    def _fetch_store_from_database(self, store_id: str) -> Optional[dict]:
        """Fetch store data from database"""
        try:
            # This would connect to the actual database
            # For now, return None to simulate database miss
            return None
        except Exception as e:
            self.logger.error(f"Database fetch error: {e}")
            return None
    
    def _update_database_user(self, user_id: str, user_data: dict):
        """Update user data in database"""
        try:
            # This would update the actual database
            pass
        except Exception as e:
            self.logger.error(f"Database update error: {e}")
    
    def _update_database_store(self, store_id: str, store_data: dict):
        """Update store data in database"""
        try:
            # This would update the actual database
            pass
        except Exception as e:
            self.logger.error(f"Database update error: {e}")
    
    def cleanup_expired_cache(self):
        """Cleanup expired cache entries"""
        if self.redis_client:
            try:
                # Get all keys
                all_keys = self.redis_client.keys("*")
                expired_count = 0
                
                for key in all_keys:
                    # Check if key is expired (Redis handles TTL automatically)
                    # This is just for monitoring
                    ttl = self.redis_client.ttl(key)
                    if ttl == -2:  # Key doesn't exist (expired)
                        expired_count += 1
                
                if expired_count > 0:
                    self.logger.info(f"Cleaned up {expired_count} expired cache entries")
                    
            except Exception as e:
                self.logger.error(f"Cache cleanup error: {e}")
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        stats = {
            'memory_cache_size': len(self._cache),
            'memory_limit': self.memory_limit,
            'redis_available': self.redis_client is not None,
            'cache_hit_ratio': 0.0
        }
        
        if self.redis_client:
            try:
                stats['redis_keys'] = len(self.redis_client.keys("*"))
            except Exception as e:
                self.logger.error(f"Error getting Redis stats: {e}")
        
        return stats
    
    def clear_all_caches(self):
        """Clear all caches (memory and Redis)"""
        # Clear memory cache
        self._cache.clear()
        self._access_order.clear()
        
        # Clear Redis cache
        if self.redis_client:
            try:
                self.redis_client.flushdb()
                print("[✅] All caches cleared")
            except Exception as e:
                self.logger.error(f"Error clearing Redis cache: {e}")

# Global SmartCacheManager instance
smart_cache_manager = SmartCacheManager()

def get_smart_cache_manager() -> SmartCacheManager:
    """Get global SmartCacheManager instance"""
    return smart_cache_manager 