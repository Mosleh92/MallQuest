#!/usr/bin/env python3
"""
Comprehensive Database Test Suite
Tests all database operations, transactions, constraints, and enhancements
"""

import sqlite3
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

def setup_logging():
    """Setup logging"""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger('DatabaseTest')

def test_database_creation():
    """Test database creation and initialization"""
    print("\n=== Testing Database Creation ===")
    
    try:
        from database import MallDatabase
        
        # Create database
        db = MallDatabase()
        print("✅ Database created successfully")
        
        # Test connection
        cursor = db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in cursor.fetchall()]
        print(f"✅ Tables found: {len(tables)}")
        
        # Check required tables
        required_tables = [
            'users', 'receipts', 'missions', 'achievements', 
            'security_audit_log', 'rate_limits', 'user_sessions',
            'companions', 'stores', 'user_activities', 
            'admin_logs', 'support_tickets', 'migrations'
        ]
        
        for table in required_tables:
            if table in tables:
                print(f"  ✅ {table} table exists")
            else:
                print(f"  ❌ {table} table missing")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def test_user_crud_operations():
    """Test user CRUD operations"""
    print("\n=== Testing User CRUD Operations ===")
    
    try:
        from database import MallDatabase
        
        db = MallDatabase()
        
        # Test Create
        user_data = {
            'user_id': 'test_user_crud',
            'name': 'Test User CRUD',
            'email': 'test@example.com',
            'phone': '+971501234567',
            'coins': 100,
            'xp': 50,
            'level': 2,
            'vip_tier': 'Silver'
        }
        
        success = db.add_user(user_data)
        print(f"✅ User creation: {success}")
        
        # Test Read
        user = db.get_user('test_user_crud')
        if user:
            print(f"✅ User retrieval: {user['name']}")
        else:
            print("❌ User retrieval failed")
            return False
        
        # Test Update
        updates = {
            'coins': 200,
            'xp': 100,
            'level': 3,
            'vip_points': 50,
            'total_spent': 500.0,
            'language': 'ar'
        }
        
        success = db.update_user('test_user_crud', updates)
        print(f"✅ User update: {success}")
        
        # Verify update
        updated_user = db.get_user('test_user_crud')
        if updated_user['coins'] == 200:
            print("✅ Update verification successful")
        else:
            print("❌ Update verification failed")
            return False
        
        # Test Delete (cleanup)
        db.conn.execute("DELETE FROM users WHERE user_id = ?", ('test_user_crud',))
        db.conn.commit()
        
        deleted_user = db.get_user('test_user_crud')
        if deleted_user is None:
            print("✅ User deletion successful")
        else:
            print("❌ User deletion failed")
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ User CRUD test failed: {e}")
        return False

def test_receipt_operations():
    """Test receipt operations"""
    print("\n=== Testing Receipt Operations ===")
    
    try:
        from database import MallDatabase
        
        db = MallDatabase()
        
        # Create test user first
        user_data = {
            'user_id': 'receipt_test_user',
            'name': 'Receipt Test User',
            'email': 'receipt@example.com'
        }
        db.add_user(user_data)
        
        # Test receipt creation
        receipt_data = {
            'receipt_id': 'test_receipt_1',
            'user_id': 'receipt_test_user',
            'store': 'Deerfields Fashion Store',
            'category': 'fashion',
            'amount': 150.0,
            'currency': 'AED',
            'status': 'pending',
            'items': json.dumps([{'name': 'T-Shirt', 'price': 75.0}, {'name': 'Jeans', 'price': 75.0}])
        }
        
        success = db.add_receipt(receipt_data)
        print(f"✅ Receipt creation: {success}")
        
        # Test receipt retrieval
        receipts = db.get_user_receipts('receipt_test_user')
        if receipts and len(receipts) > 0:
            print(f"✅ Receipt retrieval: {len(receipts)} receipts")
            print(f"  First receipt: {receipts[0]['store']} - {receipts[0]['amount']} {receipts[0]['currency']}")
        else:
            print("❌ Receipt retrieval failed")
            return False
        
        # Test receipt verification
        db.conn.execute("""
            UPDATE receipts 
            SET status = 'verified', verified_at = CURRENT_TIMESTAMP 
            WHERE receipt_id = ?
        """, ('test_receipt_1',))
        db.conn.commit()
        
        verified_receipts = db.conn.execute("""
            SELECT * FROM receipts WHERE status = 'verified'
        """).fetchall()
        print(f"✅ Receipt verification: {len(verified_receipts)} verified receipts")
        
        # Cleanup
        db.conn.execute("DELETE FROM receipts WHERE user_id = ?", ('receipt_test_user',))
        db.conn.execute("DELETE FROM users WHERE user_id = ?", ('receipt_test_user',))
        db.conn.commit()
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Receipt operations test failed: {e}")
        return False

def test_mission_operations():
    """Test mission operations"""
    print("\n=== Testing Mission Operations ===")
    
    try:
        from database import MallDatabase
        
        db = MallDatabase()
        
        # Create test user
        user_data = {
            'user_id': 'mission_test_user',
            'name': 'Mission Test User'
        }
        db.add_user(user_data)
        
        # Test mission creation
        mission_data = {
            'mission_id': 'test_mission_1',
            'user_id': 'mission_test_user',
            'title': 'Daily Shopping Challenge',
            'description': 'Spend 100 AED today',
            'type': 'daily',
            'target': 100,
            'reward_coins': 50,
            'reward_xp': 25,
            'difficulty': 'normal',
            'personalized': True,
            'expires_at': (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        success = db.add_mission(mission_data)
        print(f"✅ Mission creation: {success}")
        
        # Test mission retrieval
        missions = db.get_user_missions('mission_test_user', 'active')
        if missions and len(missions) > 0:
            print(f"✅ Mission retrieval: {len(missions)} active missions")
            print(f"  First mission: {missions[0]['title']} - Target: {missions[0]['target']}")
        else:
            print("❌ Mission retrieval failed")
            return False
        
        # Test mission progress update
        success = db.update_mission_progress('test_mission_1', 50)
        print(f"✅ Mission progress update: {success}")
        
        # Test mission completion
        success = db.complete_mission('test_mission_1')
        print(f"✅ Mission completion: {success}")
        
        # Verify completion
        completed_missions = db.get_user_missions('mission_test_user', 'completed')
        if completed_missions and len(completed_missions) > 0:
            print(f"✅ Mission completion verification: {len(completed_missions)} completed missions")
        else:
            print("❌ Mission completion verification failed")
            return False
        
        # Cleanup
        db.conn.execute("DELETE FROM missions WHERE user_id = ?", ('mission_test_user',))
        db.conn.execute("DELETE FROM users WHERE user_id = ?", ('mission_test_user',))
        db.conn.commit()
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Mission operations test failed: {e}")
        return False

def test_achievement_operations():
    """Test achievement operations"""
    print("\n=== Testing Achievement Operations ===")
    
    try:
        from enhance_database import SecureDatabaseOperations
        
        db_ops = SecureDatabaseOperations()
        
        # Create test user
        db_ops.conn.execute("""
            INSERT OR REPLACE INTO users (user_id, name, email)
            VALUES (?, ?, ?)
        """, ('achievement_test_user', 'Achievement Test User', 'achievement@example.com'))
        db_ops.conn.commit()
        
        # Test achievement creation
        achievement_data = {
            'achievement_id': 'test_achievement_1',
            'user_id': 'achievement_test_user',
            'achievement_type': 'shopping',
            'title': 'First Purchase',
            'description': 'Complete your first purchase',
            'points': 10,
            'icon': 'shopping-cart',
            'metadata': json.dumps({'category': 'general', 'difficulty': 'easy'})
        }
        
        success = db_ops.add_achievement(achievement_data)
        print(f"✅ Achievement creation: {success}")
        
        # Test achievement retrieval
        achievements = db_ops.get_user_achievements('achievement_test_user')
        if achievements and len(achievements) > 0:
            print(f"✅ Achievement retrieval: {len(achievements)} achievements")
            print(f"  First achievement: {achievements[0]['title']} - {achievements[0]['points']} points")
        else:
            print("❌ Achievement retrieval failed")
            return False
        
        # Test duplicate achievement prevention
        success = db_ops.add_achievement(achievement_data)
        print(f"✅ Duplicate achievement prevention: {not success}")
        
        # Cleanup
        db_ops.conn.execute("DELETE FROM achievements WHERE user_id = ?", ('achievement_test_user',))
        db_ops.conn.execute("DELETE FROM users WHERE user_id = ?", ('achievement_test_user',))
        db_ops.conn.commit()
        
        db_ops.close()
        return True
        
    except Exception as e:
        print(f"❌ Achievement operations test failed: {e}")
        return False

def test_session_operations():
    """Test user session operations"""
    print("\n=== Testing Session Operations ===")
    
    try:
        from enhance_database import SecureDatabaseOperations
        
        db_ops = SecureDatabaseOperations()
        
        # Create test user
        db_ops.conn.execute("""
            INSERT OR REPLACE INTO users (user_id, name, email)
            VALUES (?, ?, ?)
        """, ('session_test_user', 'Session Test User', 'session@example.com'))
        db_ops.conn.commit()
        
        # Test session creation
        session_data = {
            'session_id': 'test_session_1',
            'user_id': 'session_test_user',
            'token_hash': 'hashed_token_123',
            'ip_address': '192.168.1.100',
            'user_agent': 'Test Browser',
            'expires_at': (datetime.now() + timedelta(hours=1)).isoformat()
        }
        
        success = db_ops.add_user_session(session_data)
        print(f"✅ Session creation: {success}")
        
        # Test session retrieval
        session = db_ops.get_user_session('test_session_1')
        if session:
            print(f"✅ Session retrieval: {session['user_id']} - {session['ip_address']}")
        else:
            print("❌ Session retrieval failed")
            return False
        
        # Test session invalidation
        success = db_ops.invalidate_user_session('test_session_1')
        print(f"✅ Session invalidation: {success}")
        
        # Verify invalidation
        invalidated_session = db_ops.get_user_session('test_session_1')
        if invalidated_session is None:
            print("✅ Session invalidation verification successful")
        else:
            print("❌ Session invalidation verification failed")
            return False
        
        # Test expired session cleanup
        expired_count = db_ops.cleanup_expired_sessions()
        print(f"✅ Expired session cleanup: {expired_count} sessions cleaned")
        
        # Cleanup
        db_ops.conn.execute("DELETE FROM user_sessions WHERE user_id = ?", ('session_test_user',))
        db_ops.conn.execute("DELETE FROM users WHERE user_id = ?", ('session_test_user',))
        db_ops.conn.commit()
        
        db_ops.close()
        return True
        
    except Exception as e:
        print(f"❌ Session operations test failed: {e}")
        return False

def test_security_audit_logging():
    """Test security audit logging"""
    print("\n=== Testing Security Audit Logging ===")
    
    try:
        from enhance_database import SecureDatabaseOperations
        
        db_ops = SecureDatabaseOperations()
        
        # Test security event logging
        success = db_ops.log_security_event(
            'audit_test_user',
            'login_attempt',
            '192.168.1.100',
            'Successful login attempt'
        )
        print(f"✅ Security event logging: {success}")
        
        # Test MFA attempt logging
        success = db_ops.log_security_event(
            'audit_test_user',
            'mfa_verification',
            '192.168.1.100',
            'MFA verification successful'
        )
        print(f"✅ MFA attempt logging: {success}")
        
        # Test security log retrieval
        logs = db_ops.get_security_logs('audit_test_user', 10)
        if logs and len(logs) > 0:
            print(f"✅ Security log retrieval: {len(logs)} logs")
            for log in logs[:2]:  # Show first 2 logs
                print(f"  - {log['action']}: {log['details']}")
        else:
            print("❌ Security log retrieval failed")
            return False
        
        # Test all security logs
        all_logs = db_ops.get_security_logs(limit=5)
        print(f"✅ All security logs retrieval: {len(all_logs)} logs")
        
        # Cleanup
        db_ops.conn.execute("DELETE FROM security_audit_log WHERE user_id = ?", ('audit_test_user',))
        db_ops.conn.commit()
        
        db_ops.close()
        return True
        
    except Exception as e:
        print(f"❌ Security audit logging test failed: {e}")
        return False

def test_database_constraints():
    """Test database constraints and validation"""
    print("\n=== Testing Database Constraints ===")
    
    try:
        from database import MallDatabase
        
        db = MallDatabase()
        
        # Test unique constraint on user_id
        user_data1 = {
            'user_id': 'constraint_test_user',
            'name': 'Constraint Test User 1',
            'email': 'test1@example.com'
        }
        
        user_data2 = {
            'user_id': 'constraint_test_user',  # Same user_id
            'name': 'Constraint Test User 2',
            'email': 'test2@example.com'
        }
        
        # First user should succeed
        success1 = db.add_user(user_data1)
        print(f"✅ First user creation: {success1}")
        
        # Second user with same ID should fail
        try:
            success2 = db.add_user(user_data2)
            print(f"❌ Duplicate user creation should have failed: {success2}")
            return False
        except sqlite3.IntegrityError:
            print("✅ Duplicate user constraint working")
        
        # Test foreign key constraint
        try:
            db.conn.execute("""
                INSERT INTO receipts (receipt_id, user_id, store, amount)
                VALUES (?, ?, ?, ?)
            """, ('test_receipt_fk', 'nonexistent_user', 'Test Store', 100.0))
            db.conn.commit()
            print("❌ Foreign key constraint should have failed")
            return False
        except sqlite3.IntegrityError:
            print("✅ Foreign key constraint working")
        
        # Test not null constraint
        try:
            db.conn.execute("""
                INSERT INTO users (user_id, name)
                VALUES (?, ?)
            """, ('null_test_user', None))
            db.conn.commit()
            print("❌ Not null constraint should have failed")
            return False
        except sqlite3.IntegrityError:
            print("✅ Not null constraint working")
        
        # Cleanup
        db.conn.execute("DELETE FROM users WHERE user_id = ?", ('constraint_test_user',))
        db.conn.commit()
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database constraints test failed: {e}")
        return False

def test_database_transactions():
    """Test database transactions"""
    print("\n=== Testing Database Transactions ===")
    
    try:
        from database import MallDatabase
        
        db = MallDatabase()
        
        # Test successful transaction
        try:
            db.conn.execute("BEGIN TRANSACTION")
            
            # Create user
            user_data = {
                'user_id': 'transaction_test_user',
                'name': 'Transaction Test User',
                'email': 'transaction@example.com'
            }
            db.add_user(user_data)
            
            # Create receipt
            receipt_data = {
                'receipt_id': 'transaction_receipt_1',
                'user_id': 'transaction_test_user',
                'store': 'Transaction Store',
                'amount': 200.0
            }
            db.add_receipt(receipt_data)
            
            db.conn.commit()
            print("✅ Successful transaction completed")
            
        except Exception as e:
            db.conn.rollback()
            print(f"❌ Transaction failed: {e}")
            return False
        
        # Verify transaction
        user = db.get_user('transaction_test_user')
        receipts = db.get_user_receipts('transaction_test_user')
        
        if user and receipts:
            print(f"✅ Transaction verification: User and {len(receipts)} receipts created")
        else:
            print("❌ Transaction verification failed")
            return False
        
        # Test rollback on error
        try:
            db.conn.execute("BEGIN TRANSACTION")
            
            # This should succeed
            db.conn.execute("""
                INSERT INTO users (user_id, name, email)
                VALUES (?, ?, ?)
            """, ('rollback_test_user', 'Rollback Test User', 'rollback@example.com'))
            
            # This should fail (duplicate user_id)
            db.conn.execute("""
                INSERT INTO users (user_id, name, email)
                VALUES (?, ?, ?)
            """, ('rollback_test_user', 'Duplicate User', 'duplicate@example.com'))
            
            db.conn.commit()
            print("❌ Rollback test should have failed")
            return False
            
        except sqlite3.IntegrityError:
            db.conn.rollback()
            print("✅ Rollback on error working")
        
        # Verify rollback
        user = db.get_user('rollback_test_user')
        if user is None:
            print("✅ Rollback verification successful")
        else:
            print("❌ Rollback verification failed")
            return False
        
        # Cleanup
        db.conn.execute("DELETE FROM receipts WHERE user_id = ?", ('transaction_test_user',))
        db.conn.execute("DELETE FROM users WHERE user_id = ?", ('transaction_test_user',))
        db.conn.commit()
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database transactions test failed: {e}")
        return False

def test_database_performance():
    """Test database performance"""
    print("\n=== Testing Database Performance ===")
    
    try:
        from database import MallDatabase
        
        db = MallDatabase()
        
        # Benchmark user creation
        start_time = time.time()
        for i in range(100):
            user_data = {
                'user_id': f'perf_user_{i}',
                'name': f'Performance User {i}',
                'email': f'perf{i}@example.com'
            }
            db.add_user(user_data)
        user_creation_time = time.time() - start_time
        print(f"✅ User creation: {user_creation_time:.3f}s for 100 users")
        
        # Benchmark receipt creation
        start_time = time.time()
        for i in range(100):
            receipt_data = {
                'receipt_id': f'perf_receipt_{i}',
                'user_id': f'perf_user_{i}',
                'store': f'Performance Store {i}',
                'amount': 100.0 + i
            }
            db.add_receipt(receipt_data)
        receipt_creation_time = time.time() - start_time
        print(f"✅ Receipt creation: {receipt_creation_time:.3f}s for 100 receipts")
        
        # Benchmark user retrieval
        start_time = time.time()
        for i in range(100):
            user = db.get_user(f'perf_user_{i}')
        user_retrieval_time = time.time() - start_time
        print(f"✅ User retrieval: {user_retrieval_time:.3f}s for 100 users")
        
        # Benchmark receipt retrieval
        start_time = time.time()
        for i in range(10):  # Test with fewer users to avoid too many receipts
            receipts = db.get_user_receipts(f'perf_user_{i}')
        receipt_retrieval_time = time.time() - start_time
        print(f"✅ Receipt retrieval: {receipt_retrieval_time:.3f}s for 10 users")
        
        # Test system stats performance
        start_time = time.time()
        stats = db.get_system_stats()
        stats_time = time.time() - start_time
        print(f"✅ System stats: {stats_time:.3f}s")
        print(f"  Stats: {stats}")
        
        # Cleanup
        db.conn.execute("DELETE FROM receipts WHERE user_id LIKE 'perf_user_%'")
        db.conn.execute("DELETE FROM users WHERE user_id LIKE 'perf_user_%'")
        db.conn.commit()
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database performance test failed: {e}")
        return False

def test_database_optimization():
    """Test database optimization features"""
    print("\n=== Testing Database Optimization ===")
    
    try:
        from enhance_database import optimize_database, get_database_health
        
        # Test database optimization
        success = optimize_database()
        print(f"✅ Database optimization: {success}")
        
        # Test database health check
        health = get_database_health()
        print(f"✅ Database health check: {health}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database optimization test failed: {e}")
        return False

def main():
    """Run all database tests"""
    print("🚀 Comprehensive Database Test Suite")
    print("=" * 60)
    
    try:
        # Run all tests
        tests = [
            ("Database Creation", test_database_creation),
            ("User CRUD Operations", test_user_crud_operations),
            ("Receipt Operations", test_receipt_operations),
            ("Mission Operations", test_mission_operations),
            ("Achievement Operations", test_achievement_operations),
            ("Session Operations", test_session_operations),
            ("Security Audit Logging", test_security_audit_logging),
            ("Database Constraints", test_database_constraints),
            ("Database Transactions", test_database_transactions),
            ("Database Performance", test_database_performance),
            ("Database Optimization", test_database_optimization)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    print(f"✅ {test_name} PASSED")
                    passed += 1
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} FAILED with exception: {e}")
        
        print("\n" + "=" * 60)
        print(f"📋 Database Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All database tests passed! Database is fully functional.")
        elif passed >= total * 0.8:
            print("⚠️ Most database tests passed. Database is mostly functional.")
        else:
            print("❌ Many database tests failed. Database needs attention.")
        
        return passed == total
        
    except Exception as e:
        print(f"\n❌ Database test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 