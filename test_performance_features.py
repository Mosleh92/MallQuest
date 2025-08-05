#!/usr/bin/env python3
"""
Test script for performance features of the mall gamification system
Tests all performance optimization classes and functionality.
"""

import time
import asyncio
import threading
from performance_module import (
    PerformanceManager, MemoryEfficientEffects, CachedDatabase,
    AsyncTaskManager, OptimizedGraphicsEngine, PerformanceMonitor,
    record_performance_event, cleanup_performance_resources
)

def test_performance_manager():
    """Test PerformanceManager functionality"""
    print("\n=== Testing PerformanceManager ===")
    
    pm = PerformanceManager()
    
    # Test cache operations
    print("Testing cache operations...")
    success = pm.set_cache("test_key", "test_value", ttl=60)
    print(f"Cache set: {success}")
    
    value = pm.get_cache("test_key")
    print(f"Cache get: {value}")
    
    # Test cache clearing
    success = pm.clear_cache("test_key")
    print(f"Cache clear: {success}")
    
    print("✅ PerformanceManager tests completed")

def test_memory_efficient_effects():
    """Test MemoryEfficientEffects functionality"""
    print("\n=== Testing MemoryEfficientEffects ===")
    
    effects = MemoryEfficientEffects(max_effects=5)
    
    # Add effects
    print("Adding effects...")
    for i in range(3):
        effects.add_effect({
            "type": f"test_effect_{i}",
            "duration": 2.0,
            "data": {"value": i}
        })
    
    print(f"Active effects: {len(effects.active_effects)}")
    
    # Wait for cleanup
    print("Waiting for effect cleanup...")
    time.sleep(3)
    
    print(f"Active effects after cleanup: {len(effects.active_effects)}")
    
    # Stop cleanup thread
    effects.stop_cleanup()
    print("✅ MemoryEfficientEffects tests completed")

def test_cached_database():
    """Test CachedDatabase functionality"""
    print("\n=== Testing CachedDatabase ===")
    
    # Create a test database
    db = CachedDatabase("test_performance.db")
    
    # Test user caching
    print("Testing user caching...")
    
    # Create a test user
    db.execute_safe_query('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            coins INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert test user
    db.execute_safe_query(
        "INSERT OR REPLACE INTO users (user_id, name, coins, xp) VALUES (?, ?, ?, ?)",
        ("test_user_1", "Test User", 100, 50)
    )
    
    # Test cached get
    user = db.get_user("test_user_1")
    print(f"Cached user: {user}")
    
    # Test batch update
    print("Testing batch update...")
    updates = [
        ("test_user_1", {"coins": 150, "xp": 75}),
        ("test_user_2", {"coins": 200, "xp": 100})
    ]
    
    # Insert second user
    db.execute_safe_query(
        "INSERT OR REPLACE INTO users (user_id, name, coins, xp) VALUES (?, ?, ?, ?)",
        ("test_user_2", "Test User 2", 200, 100)
    )
    
    success = db.batch_update_users(updates)
    print(f"Batch update success: {success}")
    
    # Verify updates
    user1 = db.get_user("test_user_1")
    user2 = db.get_user("test_user_2")
    print(f"Updated user1: {user1}")
    print(f"Updated user2: {user2}")
    
    print("✅ CachedDatabase tests completed")

async def test_async_task_manager():
    """Test AsyncTaskManager functionality"""
    print("\n=== Testing AsyncTaskManager ===")
    
    atm = AsyncTaskManager()
    
    # Test async receipt processing
    print("Testing async receipt processing...")
    
    result1 = await atm.process_receipt_async("test_user", 50.0, "Deerfields Store")
    print(f"Receipt 1 result: {result1}")
    
    result2 = await atm.process_receipt_async("test_user", 25.0, "Invalid Store")
    print(f"Receipt 2 result: {result2}")
    
    # Test concurrent processing
    print("Testing concurrent processing...")
    tasks = []
    for i in range(3):
        task = atm.process_receipt_async(f"user_{i}", 10.0 * (i + 1), "Deerfields Store")
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    for i, result in enumerate(results):
        print(f"Concurrent result {i}: {result}")
    
    # Shutdown
    atm.shutdown()
    print("✅ AsyncTaskManager tests completed")

def test_optimized_graphics_engine():
    """Test OptimizedGraphicsEngine functionality"""
    print("\n=== Testing OptimizedGraphicsEngine ===")
    
    graphics = OptimizedGraphicsEngine()
    
    # Test effect triggering
    print("Testing effect triggering...")
    
    for i in range(5):
        result = graphics.trigger_effect("coin_earned", coins=10 * (i + 1), user_id=f"user_{i}")
        print(f"Effect {i} result: {result}")
    
    # Test rendering
    print("Testing rendering...")
    for i in range(3):
        render_result = graphics.render_frame()
        print(f"Render {i}: {render_result}")
        time.sleep(0.1)
    
    # Test throttling
    print("Testing effect throttling...")
    for i in range(10):
        result = graphics.trigger_effect("test_effect", duration=1.0)
        print(f"Throttle test {i}: {result}")
    
    # Shutdown
    graphics.shutdown()
    print("✅ OptimizedGraphicsEngine tests completed")

def test_performance_monitor():
    """Test PerformanceMonitor functionality"""
    print("\n=== Testing PerformanceMonitor ===")
    
    monitor = PerformanceMonitor()
    
    # Record some requests
    print("Recording performance metrics...")
    for i in range(10):
        response_time = 0.1 + (i * 0.01)  # Simulate varying response times
        monitor.record_request(response_time)
        time.sleep(0.01)
    
    # Get performance report
    report = monitor.get_performance_report()
    print(f"Performance report: {report}")
    
    # Log metrics
    monitor.log_performance_metrics()
    
    print("✅ PerformanceMonitor tests completed")

def test_performance_event_recording():
    """Test performance event recording"""
    print("\n=== Testing Performance Event Recording ===")
    
    # Record various events
    record_performance_event("test_event_1", 0.15)
    record_performance_event("test_event_2", 0.25)
    record_performance_event("test_event_3")  # No duration
    
    print("✅ Performance event recording tests completed")

async def run_all_tests():
    """Run all performance tests"""
    print("🚀 Starting Performance Features Tests")
    print("=" * 50)
    
    try:
        # Run synchronous tests
        test_performance_manager()
        test_memory_efficient_effects()
        test_cached_database()
        test_optimized_graphics_engine()
        test_performance_monitor()
        test_performance_event_recording()
        
        # Run async tests
        await test_async_task_manager()
        
        print("\n" + "=" * 50)
        print("✅ All performance tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up performance resources...")
        cleanup_performance_resources()

if __name__ == "__main__":
    # Run the tests
    asyncio.run(run_all_tests()) 