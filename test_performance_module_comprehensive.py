#!/usr/bin/env python3
"""
Comprehensive Test for Performance Module
Tests all components: PerformanceManager, MemoryEfficientEffects, CachedDatabase,
AsyncTaskManager, OptimizedGraphicsEngine, PerformanceMonitor, and SmartCacheManager
"""

import time
import asyncio
import threading
from performance_module import (
    PerformanceManager, MemoryEfficientEffects, CachedDatabase,
    AsyncTaskManager, OptimizedGraphicsEngine, PerformanceMonitor,
    SmartCacheManager, record_performance_event, cleanup_performance_resources,
    get_performance_manager, get_performance_monitor, get_optimized_graphics,
    get_smart_cache_manager
)

def test_performance_manager():
    """Test PerformanceManager functionality"""
    print("\n=== Testing PerformanceManager ===")
    
    pm = PerformanceManager()
    
    # Test Redis connection
    print(f"Redis available: {pm.redis_client is not None}")
    
    # Test cache operations
    test_key = "test_performance_key"
    test_value = "test_performance_value"
    
    # Set cache
    success = pm.set_cache(test_key, test_value, ttl=60)
    print(f"Cache set success: {success}")
    
    # Get cache
    cached_value = pm.get_cache(test_key)
    print(f"Cached value: {cached_value}")
    
    # Clear cache
    clear_success = pm.clear_cache(test_key)
    print(f"Cache clear success: {clear_success}")
    
    print("✅ PerformanceManager tests completed")

def test_memory_efficient_effects():
    """Test MemoryEfficientEffects functionality"""
    print("\n=== Testing MemoryEfficientEffects ===")
    
    effects = MemoryEfficientEffects(max_effects=5)
    
    # Add effects
    for i in range(7):  # More than max_effects to test overflow
        effect = {
            "type": f"test_effect_{i}",
            "duration": 2.0,
            "data": {"value": i}
        }
        effects.add_effect(effect)
        print(f"Added effect {i}, total active: {len(effects.active_effects)}")
    
    # Wait for some effects to expire
    print("Waiting for effects to expire...")
    time.sleep(3)
    
    # Check cleanup
    active_effects = effects.get_active_effects()
    print(f"Active effects after cleanup: {len(active_effects)}")
    
    # Stop cleanup thread
    effects.stop_cleanup()
    print("✅ MemoryEfficientEffects tests completed")

def test_cached_database():
    """Test CachedDatabase functionality"""
    print("\n=== Testing CachedDatabase ===")
    
    db = CachedDatabase(":memory:")  # Use in-memory database for testing
    
    # Create test table
    db.execute_safe_query("""
        CREATE TABLE IF NOT EXISTS test_users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            coins INTEGER DEFAULT 0
        )
    """)
    
    # Insert test data
    db.execute_safe_query(
        "INSERT OR REPLACE INTO test_users (user_id, name, coins) VALUES (?, ?, ?)",
        ("test_user_1", "Test User", 100)
    )
    
    # Test batch update
    user_updates = [
        ("test_user_1", {"coins": 150}),
        ("test_user_2", {"name": "New User", "coins": 200})
    ]
    
    batch_success = db.batch_update_users(user_updates)
    print(f"Batch update success: {batch_success}")
    
    # Test user retrieval (will use LRU cache)
    user = db.get_user("test_user_1")
    print(f"Retrieved user: {user}")
    
    print("✅ CachedDatabase tests completed")

async def test_async_task_manager():
    """Test AsyncTaskManager functionality"""
    print("\n=== Testing AsyncTaskManager ===")
    
    atm = AsyncTaskManager()
    
    # Test async receipt processing
    start_time = time.time()
    result = await atm.process_receipt_async("test_user", 100.0, "Deerfields Store")
    processing_time = time.time() - start_time
    
    print(f"Async processing result: {result}")
    print(f"Processing time: {processing_time:.3f}s")
    
    # Shutdown
    atm.shutdown()
    print("✅ AsyncTaskManager tests completed")

def test_optimized_graphics_engine():
    """Test OptimizedGraphicsEngine functionality"""
    print("\n=== Testing OptimizedGraphicsEngine ===")
    
    graphics = OptimizedGraphicsEngine()
    
    # Test effect triggering
    for i in range(3):
        result = graphics.trigger_effect("coin_collection", amount=50, duration=1.0)
        print(f"Effect {i} result: {result}")
        time.sleep(0.1)  # Small delay
    
    # Test frame rendering
    render_result = graphics.render_frame()
    print(f"Render result: {render_result}")
    
    # Shutdown
    graphics.shutdown()
    print("✅ OptimizedGraphicsEngine tests completed")

def test_performance_monitor():
    """Test PerformanceMonitor functionality"""
    print("\n=== Testing PerformanceMonitor ===")
    
    monitor = PerformanceMonitor()
    
    # Record some requests
    for i in range(5):
        response_time = 0.1 + (i * 0.05)  # Simulate varying response times
        monitor.record_request(response_time)
        time.sleep(0.1)
    
    # Get performance report
    report = monitor.get_performance_report()
    print(f"Performance report: {report}")
    
    # Log metrics
    monitor.log_performance_metrics()
    print("✅ PerformanceMonitor tests completed")

def test_smart_cache_manager():
    """Test SmartCacheManager functionality"""
    print("\n=== Testing SmartCacheManager ===")
    
    cache = SmartCacheManager(memory_limit=3, redis_ttl=60)
    
    # Test user data operations
    test_user_data = {"user_id": "test_user", "coins": 100, "level": 5}
    
    # Set user data
    success = cache.set_user_data("test_user", test_user_data)
    print(f"Set user data success: {success}")
    
    # Get user data
    retrieved_data = cache.get_user_data("test_user")
    print(f"Retrieved user data: {retrieved_data}")
    
    # Test store data operations
    test_store_data = {"store_id": "test_store", "name": "Test Store", "category": "fashion"}
    
    # Set store data
    success = cache.set_store_data("test_store", test_store_data)
    print(f"Set store data success: {success}")
    
    # Get store data
    retrieved_store_data = cache.get_store_data("test_store")
    print(f"Retrieved store data: {retrieved_store_data}")
    
    # Test cache stats
    stats = cache.get_cache_stats()
    print(f"Cache stats: {stats}")
    
    # Test cache overflow (LRU eviction)
    for i in range(5):
        cache.set_user_data(f"user_{i}", {"coins": i * 10})
    
    final_stats = cache.get_cache_stats()
    print(f"Final cache stats: {final_stats}")
    
    # Cleanup
    cache.clear_all_caches()
    print("✅ SmartCacheManager tests completed")

def test_global_instances():
    """Test global instances and convenience functions"""
    print("\n=== Testing Global Instances ===")
    
    # Test global instances
    pm = get_performance_manager()
    monitor = get_performance_monitor()
    graphics = get_optimized_graphics()
    cache = get_smart_cache_manager()
    
    print(f"Global PerformanceManager: {type(pm)}")
    print(f"Global PerformanceMonitor: {type(monitor)}")
    print(f"Global OptimizedGraphicsEngine: {type(graphics)}")
    print(f"Global SmartCacheManager: {type(cache)}")
    
    # Test performance event recording
    record_performance_event("test_event", 0.5)
    print("✅ Global instances tests completed")

def test_integration():
    """Test integration between components"""
    print("\n=== Testing Integration ===")
    
    # Test performance monitoring with graphics
    graphics = get_optimized_graphics()
    monitor = get_performance_monitor()
    
    # Trigger effects and monitor performance
    for i in range(3):
        start_time = time.time()
        result = graphics.trigger_effect("integration_test", duration=1.0)
        processing_time = time.time() - start_time
        
        monitor.record_request(processing_time)
        record_performance_event("integration_effect", processing_time)
        
        print(f"Integration test {i}: {result}")
    
    # Get final performance report
    report = monitor.get_performance_report()
    print(f"Integration performance report: {report}")
    
    print("✅ Integration tests completed")

async def main():
    """Run all performance tests"""
    print("🚀 Starting Comprehensive Performance Module Tests")
    print("=" * 60)
    
    try:
        # Test individual components
        test_performance_manager()
        test_memory_efficient_effects()
        test_cached_database()
        await test_async_task_manager()
        test_optimized_graphics_engine()
        test_performance_monitor()
        test_smart_cache_manager()
        test_global_instances()
        test_integration()
        
        print("\n" + "=" * 60)
        print("✅ All Performance Module Tests Completed Successfully!")
        
        # Final cleanup
        cleanup_performance_resources()
        print("✅ Performance resources cleaned up")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 