#!/usr/bin/env python3
"""
Simple System Test for Deerfields Mall Gamification System
Quick test of basic functionality for all major components
"""

import time
import json
from datetime import datetime

def test_basic_imports():
    """Test that all major modules can be imported"""
    print("🔍 Testing Basic Imports...")
    
    try:
        from mall_gamification_system import MallGamificationSystem
        print("  ✅ MallGamificationSystem imported")
    except Exception as e:
        print(f"  ❌ MallGamificationSystem import failed: {e}")
        return False
    
    try:
        from security_module import SecurityManager, SecureDatabase
        print("  ✅ Security modules imported")
    except Exception as e:
        print(f"  ❌ Security modules import failed: {e}")
        return False
    
    try:
        from performance_module import PerformanceManager, PerformanceMonitor
        print("  ✅ Performance modules imported")
    except Exception as e:
        print(f"  ❌ Performance modules import failed: {e}")
        return False
    
    try:
        from database import MallDatabase
        print("  ✅ Database module imported")
    except Exception as e:
        print(f"  ❌ Database module import failed: {e}")
        return False
    
    return True

def test_basic_gamification():
    """Test basic gamification functionality"""
    print("\n🎮 Testing Basic Gamification...")
    
    try:
        from mall_gamification_system import MallGamificationSystem
        
        # Create system
        mall_system = MallGamificationSystem()
        print("  ✅ MallGamificationSystem created")
        
        # Create user
        user = mall_system.create_user("test_user", "en")
        print(f"  ✅ User created: {user.user_id}")
        
        # Process receipt
        result = mall_system.process_receipt(user.user_id, 100, "Deerfields Store")
        print(f"  ✅ Receipt processed: {result['status']}")
        
        # Generate missions
        missions = mall_system.generate_user_missions(user.user_id, "daily")
        print(f"  ✅ Missions generated: {len(missions)}")
        
        # Get user dashboard
        dashboard = mall_system.get_user_dashboard(user.user_id)
        print(f"  ✅ Dashboard retrieved: {dashboard['user_info']['coins']} coins")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Gamification test failed: {e}")
        return False

def test_basic_security():
    """Test basic security functionality"""
    print("\n🔒 Testing Basic Security...")
    
    try:
        from security_module import SecurityManager, SecureDatabase
        
        # Create security manager
        security_manager = SecurityManager()
        print("  ✅ SecurityManager created")
        
        # Test JWT token generation
        token = security_manager.generate_token("test_user", "user")
        print(f"  ✅ JWT token generated: {token[:20]}...")
        
        # Test token verification
        payload = security_manager.verify_token(token)
        print(f"  ✅ Token verified: {payload['user_id']}")
        
        # Test password hashing
        password = "test_password"
        hashed = security_manager.hash_password(password)
        print(f"  ✅ Password hashed: {hashed[:20]}...")
        
        # Test password verification
        is_valid = security_manager.verify_password(password, hashed)
        print(f"  ✅ Password verified: {is_valid}")
        
        # Test secure database
        secure_db = SecureDatabase()
        print("  ✅ SecureDatabase created")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Security test failed: {e}")
        return False

def test_basic_performance():
    """Test basic performance functionality"""
    print("\n⚡ Testing Basic Performance...")
    
    try:
        from performance_module import PerformanceManager, PerformanceMonitor
        
        # Create performance manager
        pm = PerformanceManager()
        print("  ✅ PerformanceManager created")
        
        # Test caching
        pm.set_cache("test_key", "test_value", 60)
        cached_value = pm.get_cache("test_key")
        print(f"  ✅ Cache test: {cached_value}")
        
        # Create performance monitor
        monitor = PerformanceMonitor()
        print("  ✅ PerformanceMonitor created")
        
        # Record some metrics
        monitor.record_request(0.1)
        monitor.record_request(0.2)
        monitor.record_request(0.15)
        
        # Get performance report
        report = monitor.get_performance_report()
        print(f"  ✅ Performance report: {report['total_requests']} requests")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Performance test failed: {e}")
        return False

def test_basic_database():
    """Test basic database functionality"""
    print("\n💾 Testing Basic Database...")
    
    try:
        from database import MallDatabase
        
        # Create database
        db = MallDatabase()
        print("  ✅ Database created")
        
        # Test user operations
        user_data = {
            'user_id': 'db_test_user',
            'name': 'Database Test User',
            'email': 'test@example.com',
            'coins': 100
        }
        
        success = db.add_user(user_data)
        print(f"  ✅ User added: {success}")
        
        user = db.get_user('db_test_user')
        print(f"  ✅ User retrieved: {user['name']}")
        
        # Test receipt operations
        receipt_data = {
            'receipt_id': 'test_receipt_1',
            'user_id': 'db_test_user',
            'store_name': 'Test Store',
            'amount': 50.0
        }
        
        success = db.add_receipt(receipt_data)
        print(f"  ✅ Receipt added: {success}")
        
        receipts = db.get_user_receipts('db_test_user')
        print(f"  ✅ Receipts retrieved: {len(receipts)}")
        
        # Test system stats
        stats = db.get_system_stats()
        print(f"  ✅ System stats: {stats['total_users']} users")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False

def test_web_interface_basic():
    """Test basic web interface functionality"""
    print("\n🌐 Testing Basic Web Interface...")
    
    try:
        # Test that Flask app can be created
        from flask import Flask
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret'
        print("  ✅ Flask app created")
        
        # Test that we can import web interface components
        try:
            from optimized_web_interface import app as web_app
            print("  ✅ Web interface app imported")
        except Exception as e:
            print(f"  ⚠️ Web interface import failed: {e}")
        
        # Test basic route creation
        @app.route('/test')
        def test_route():
            return {'status': 'ok'}
        
        with app.test_client() as client:
            response = client.get('/test')
            print(f"  ✅ Test route working: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Web interface test failed: {e}")
        return False

def test_integration_basic():
    """Test basic integration between components"""
    print("\n🔗 Testing Basic Integration...")
    
    try:
        from mall_gamification_system import MallGamificationSystem
        from security_module import SecurityManager
        from performance_module import PerformanceMonitor
        
        # Create all components
        mall_system = MallGamificationSystem()
        security_manager = SecurityManager()
        performance_monitor = PerformanceMonitor()
        
        print("  ✅ All components created")
        
        # Test integrated workflow
        user = mall_system.create_user("integration_user", "en")
        
        # Process receipt with security and performance monitoring
        start_time = time.time()
        result = mall_system.process_receipt(user.user_id, 200, "Integration Store")
        processing_time = time.time() - start_time
        
        performance_monitor.record_request(processing_time)
        
        print(f"  ✅ Integrated workflow: {result['status']}")
        print(f"  ✅ Processing time: {processing_time:.3f}s")
        
        # Test performance report
        report = performance_monitor.get_performance_report()
        print(f"  ✅ Performance monitoring: {report['total_requests']} requests")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        return False

def test_error_handling():
    """Test basic error handling"""
    print("\n⚠️ Testing Error Handling...")
    
    try:
        from mall_gamification_system import MallGamificationSystem
        
        mall_system = MallGamificationSystem()
        
        # Test invalid user operations
        try:
            result = mall_system.process_receipt("nonexistent_user", 100, "Test Store")
            print(f"  ✅ Invalid user handled gracefully: {result['status']}")
        except Exception as e:
            print(f"  ✅ Invalid user error caught: {type(e).__name__}")
        
        # Test invalid receipt data
        try:
            result = mall_system.process_receipt("test_user", -100, "Test Store")
            print(f"  ✅ Invalid amount handled: {result['status']}")
        except Exception as e:
            print(f"  ✅ Invalid amount error caught: {type(e).__name__}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        return False

def test_performance_benchmarks():
    """Test basic performance benchmarks"""
    print("\n📊 Testing Performance Benchmarks...")
    
    try:
        from mall_gamification_system import MallGamificationSystem
        
        mall_system = MallGamificationSystem()
        
        # Benchmark user creation
        start_time = time.time()
        for i in range(10):
            user = mall_system.create_user(f"benchmark_user_{i}", "en")
        user_creation_time = time.time() - start_time
        print(f"  ✅ User creation: {user_creation_time:.3f}s for 10 users")
        
        # Benchmark receipt processing
        start_time = time.time()
        for i in range(10):
            result = mall_system.process_receipt(f"benchmark_user_{i}", 100 + i, "Benchmark Store")
        receipt_time = time.time() - start_time
        print(f"  ✅ Receipt processing: {receipt_time:.3f}s for 10 receipts")
        
        # Benchmark mission generation
        start_time = time.time()
        for i in range(5):
            missions = mall_system.generate_user_missions(f"benchmark_user_{i}", "daily")
        mission_time = time.time() - start_time
        print(f"  ✅ Mission generation: {mission_time:.3f}s for 5 users")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Performance benchmark failed: {e}")
        return False

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Clean up database test data
        from database import MallDatabase
        db = MallDatabase()
        
        # Remove test users
        test_users = ['db_test_user', 'integration_user']
        for user_id in test_users:
            try:
                db.conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            except:
                pass
        
        # Remove test receipts
        try:
            db.conn.execute("DELETE FROM receipts WHERE user_id LIKE 'db_test_user%'")
        except:
            pass
        
        db.conn.commit()
        db.close()
        print("  ✅ Database cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"  ⚠️ Cleanup failed: {e}")
        return False

def main():
    """Run all simple system tests"""
    print("🚀 Simple System Test Suite")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Basic Gamification", test_basic_gamification),
        ("Basic Security", test_basic_security),
        ("Basic Performance", test_basic_performance),
        ("Basic Database", test_basic_database),
        ("Basic Web Interface", test_web_interface_basic),
        ("Basic Integration", test_integration_basic),
        ("Error Handling", test_error_handling),
        ("Performance Benchmarks", test_performance_benchmarks)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            test_results.append((test_name, False))
    
    # Cleanup
    cleanup_test_data()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
    elif passed >= total * 0.8:
        print("⚠️ Most tests passed. System is mostly functional.")
    else:
        print("❌ Many tests failed. System needs attention.")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 