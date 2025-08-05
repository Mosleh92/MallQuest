#!/usr/bin/env python3
"""
Simple Performance Test for Mall Gamification System
Basic test to verify performance module functionality without complex output.
"""

print("🚀 Starting Simple Performance Test")
print("=" * 40)

try:
    # Test basic imports
    print("Testing imports...")
    from performance_module import (
        PerformanceManager, MemoryEfficientEffects, 
        PerformanceMonitor, record_performance_event
    )
    print("✅ Imports successful")
    
    # Test PerformanceManager
    print("\nTesting PerformanceManager...")
    pm = PerformanceManager()
    print("✅ PerformanceManager created")
    
    # Test MemoryEfficientEffects
print("\nTesting MemoryEfficientEffects...")
effects = MemoryEfficientEffects(max_effects=3)
    effects.add_effect({"type": "test", "duration": 1.0})
    print(f"✅ Effects manager created with {len(effects.active_effects)} effects")
    effects.stop_cleanup()
    
    # Test PerformanceMonitor
    print("\nTesting PerformanceMonitor...")
    monitor = PerformanceMonitor()
    monitor.record_request(0.15)
    report = monitor.get_performance_report()
    print(f"✅ Performance monitor created, report: {report}")
    
    # Test event recording
    print("\nTesting event recording...")
    record_performance_event("test_event", 0.25)
    print("✅ Event recording successful")
    
    print("\n" + "=" * 40)
    print("✅ All basic performance tests passed!")
    
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc() 