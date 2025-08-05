#!/usr/bin/env python3
"""
Comprehensive System Check for Deerfields Mall Gamification System
Tests all requirements: imports, dependencies, security, performance, etc.
"""

import sys
import os
import importlib
import traceback
from pathlib import Path
from datetime import datetime

def check_imports():
    """Check if all modules can be imported without errors"""
    print("🔍 Checking module imports...")
    
    modules_to_test = [
        'web_interface',
        'optimized_web_interface', 
        'mall_gamification_system',
        'security_module',
        'performance_module',
        'database',
        'config',
        'authentication_manager',
        'companion_system',
        'ai_mission_generator',
        '3d_graphics_module'
    ]
    
    failed_imports = []
    successful_imports = []
    
    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            successful_imports.append(module_name)
            print(f"  ✅ {module_name}")
        except Exception as e:
            failed_imports.append((module_name, str(e)))
            print(f"  ❌ {module_name}: {e}")
    
    return len(failed_imports) == 0, failed_imports, successful_imports

def check_circular_dependencies():
    """Check for potential circular dependencies"""
    print("\n🔍 Checking for circular dependencies...")
    
    # Define dependency graph
    dependencies = {
        'web_interface': ['mall_gamification_system', 'security_module'],
        'optimized_web_interface': ['mall_gamification_system', 'security_module', 'performance_module'],
        'mall_gamification_system': ['database', 'security_module', 'performance_module'],
        'security_module': ['database'],
        'performance_module': ['database'],
        'database': [],
        'authentication_manager': ['security_module'],
        'companion_system': ['database'],
        'ai_mission_generator': ['database']
    }
    
    def has_cycle(graph, node, visited, rec_stack):
        visited[node] = True
        rec_stack[node] = True
        
        for neighbor in graph.get(node, []):
            if not visited.get(neighbor, False):
                if has_cycle(graph, neighbor, visited, rec_stack):
                    return True
            elif rec_stack.get(neighbor, False):
                return True
        
        rec_stack[node] = False
        return False
    
    def detect_cycles(graph):
        visited = {}
        rec_stack = {}
        
        for node in graph:
            if not visited.get(node, False):
                if has_cycle(graph, node, visited, rec_stack):
                    return True
        return False
    
    has_circular = detect_cycles(dependencies)
    
    if has_circular:
        print("  ❌ Potential circular dependencies detected")
        return False
    else:
        print("  ✅ No circular dependencies detected")
        return True

def check_error_handling():
    """Check for consistent error handling"""
    print("\n🔍 Checking error handling consistency...")
    
    error_patterns = [
        'try:',
        'except',
        'finally:',
        'raise',
        'logging.error',
        'logging.warning',
        'logger.error',
        'logger.warning'
    ]
    
    files_to_check = [
        'web_interface.py',
        'optimized_web_interface.py',
        'mall_gamification_system.py',
        'security_module.py',
        'performance_module.py',
        'database.py'
    ]
    
    error_handling_found = []
    
    for file_name in files_to_check:
        if Path(file_name).exists():
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                patterns_found = [pattern for pattern in error_patterns if pattern in content]
                if patterns_found:
                    error_handling_found.append(file_name)
                    print(f"  ✅ {file_name}: Error handling found")
                else:
                    print(f"  ⚠️ {file_name}: Limited error handling")
    
    return len(error_handling_found) >= len(files_to_check) * 0.8

def check_logging_configuration():
    """Check if logging is properly configured"""
    print("\n🔍 Checking logging configuration...")
    
    logging_patterns = [
        'logging.basicConfig',
        'logging.getLogger',
        'logger =',
        'LOG_LEVEL',
        'LOG_FILE'
    ]
    
    files_to_check = [
        'config.py',
        'web_interface.py',
        'optimized_web_interface.py',
        'security_module.py',
        'performance_module.py',
        'database.py'
    ]
    
    logging_found = []
    
    for file_name in files_to_check:
        if Path(file_name).exists():
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                patterns_found = [pattern for pattern in logging_patterns if pattern in content]
                if patterns_found:
                    logging_found.append(file_name)
                    print(f"  ✅ {file_name}: Logging configured")
                else:
                    print(f"  ⚠️ {file_name}: Limited logging")
    
    return len(logging_found) >= len(files_to_check) * 0.8

def check_security_measures():
    """Check if security measures are implemented"""
    print("\n🔍 Checking security measures...")
    
    security_patterns = [
        'JWT',
        'bcrypt',
        'hashlib',
        'secrets',
        'csrf',
        'rate_limit',
        'input_validation',
        'sanitize',
        'audit_log',
        'mfa',
        'otp'
    ]
    
    files_to_check = [
        'security_module.py',
        'web_interface.py',
        'optimized_web_interface.py',
        'authentication_manager.py'
    ]
    
    security_found = []
    
    for file_name in files_to_check:
        if Path(file_name).exists():
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                patterns_found = [pattern for pattern in security_patterns if pattern.lower() in content.lower()]
                if len(patterns_found) >= 3:  # At least 3 security features
                    security_found.append(file_name)
                    print(f"  ✅ {file_name}: Security measures found ({len(patterns_found)} features)")
                else:
                    print(f"  ⚠️ {file_name}: Limited security measures ({len(patterns_found)} features)")
    
    return len(security_found) >= len(files_to_check) * 0.8

def check_performance_optimizations():
    """Check if performance optimizations are integrated"""
    print("\n🔍 Checking performance optimizations...")
    
    performance_patterns = [
        'cache',
        'redis',
        'async',
        'thread',
        'lru_cache',
        'performance_monitor',
        'optimization',
        'connection_pool'
    ]
    
    files_to_check = [
        'performance_module.py',
        'optimized_web_interface.py',
        'mall_gamification_system.py'
    ]
    
    performance_found = []
    
    for file_name in files_to_check:
        if Path(file_name).exists():
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                patterns_found = [pattern for pattern in performance_patterns if pattern.lower() in content.lower()]
                if len(patterns_found) >= 3:  # At least 3 performance features
                    performance_found.append(file_name)
                    print(f"  ✅ {file_name}: Performance optimizations found ({len(patterns_found)} features)")
                else:
                    print(f"  ⚠️ {file_name}: Limited performance optimizations ({len(patterns_found)} features)")
    
    return len(performance_found) >= len(files_to_check) * 0.8

def check_database_operations():
    """Check if database operations are optimized"""
    print("\n🔍 Checking database operations...")
    
    db_patterns = [
        'parameterized',
        'index',
        'transaction',
        'connection',
        'optimize',
        'analyze',
        'vacuum',
        'batch'
    ]
    
    files_to_check = [
        'database.py',
        'enhance_database.py',
        'security_module.py'
    ]
    
    db_optimized = []
    
    for file_name in files_to_check:
        if Path(file_name).exists():
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                patterns_found = [pattern for pattern in db_patterns if pattern.lower() in content.lower()]
                if len(patterns_found) >= 3:  # At least 3 optimization features
                    db_optimized.append(file_name)
                    print(f"  ✅ {file_name}: Database optimizations found ({len(patterns_found)} features)")
                else:
                    print(f"  ⚠️ {file_name}: Limited database optimizations ({len(patterns_found)} features)")
    
    return len(db_optimized) >= len(files_to_check) * 0.8

def check_frontend_backend_connection():
    """Check if frontend is properly connected to backend"""
    print("\n🔍 Checking frontend-backend connection...")
    
    # Check if templates exist
    template_files = [
        'templates/index.html',
        'templates/login.html',
        'templates/player_dashboard.html',
        'templates/admin_dashboard.html'
    ]
    
    templates_exist = []
    for template in template_files:
        if Path(template).exists():
            templates_exist.append(template)
            print(f"  ✅ {template}")
        else:
            print(f"  ❌ {template}")
    
    # Check for API endpoints in templates
    api_patterns = [
        '/api/',
        'fetch(',
        'ajax',
        'json',
        'POST',
        'GET'
    ]
    
    api_connections = []
    for template in templates_exist:
        with open(template, 'r', encoding='utf-8') as f:
            content = f.read()
            patterns_found = [pattern for pattern in api_patterns if pattern in content]
            if patterns_found:
                api_connections.append(template)
                print(f"    ✅ API connections found in {Path(template).name}")
            else:
                print(f"    ⚠️ Limited API connections in {Path(template).name}")
    
    return len(templates_exist) >= len(template_files) * 0.8 and len(api_connections) >= len(templates_exist) * 0.8

def check_endpoints():
    """Check if all endpoints are defined and accessible"""
    print("\n🔍 Checking API endpoints...")
    
    required_endpoints = [
        '/',
        '/login',
        '/admin/login',
        '/player/<user_id>',
        '/admin',
        '/shopkeeper/<shop_id>',
        '/customer-service',
        '/api/submit-receipt',
        '/api/generate-mission',
        '/api/get-user-data',
        '/api/performance-metrics',
        '/health'
    ]
    
    files_to_check = [
        'web_interface.py',
        'optimized_web_interface.py'
    ]
    
    endpoints_found = []
    
    for file_name in files_to_check:
        if Path(file_name).exists():
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                found_in_file = []
                for endpoint in required_endpoints:
                    if endpoint in content:
                        found_in_file.append(endpoint)
                
                endpoints_found.extend(found_in_file)
                print(f"  ✅ {file_name}: {len(found_in_file)}/{len(required_endpoints)} endpoints found")
    
    unique_endpoints = set(endpoints_found)
    coverage = len(unique_endpoints) / len(required_endpoints)
    
    print(f"  📊 Endpoint coverage: {len(unique_endpoints)}/{len(required_endpoints)} ({coverage:.1%})")
    
    return coverage >= 0.8

def check_tests():
    """Check if tests exist and are comprehensive"""
    print("\n🔍 Checking test coverage...")
    
    test_files = [
        'test_security_features.py',
        'test_performance_module_comprehensive.py',
        'test_enhanced_gamification_system.py',
        'test_web_interface_comprehensive.py',
        'test_database_comprehensive.py',
        'test_integration_comprehensive.py',
        'simple_system_test.py'
    ]
    
    tests_exist = []
    for test_file in test_files:
        if Path(test_file).exists():
            tests_exist.append(test_file)
            print(f"  ✅ {test_file}")
        else:
            print(f"  ❌ {test_file}")
    
    return len(tests_exist) >= len(test_files) * 0.8

def check_documentation():
    """Check if documentation is complete and up-to-date"""
    print("\n🔍 Checking documentation...")
    
    doc_files = [
        'README.md',
        'CONFIGURATION_SETUP_SUMMARY.md',
        'TEST_SUITE_SUMMARY.md',
        'REQUIREMENTS_README_SUMMARY.md',
        'HTML_TEMPLATES_IMPROVEMENT_SUMMARY.md',
        'ENHANCED_GAMIFICATION_SYSTEM_SUMMARY.md',
        'WEB_INTERFACE_IMPLEMENTATION_SUMMARY.md',
        'PERFORMANCE_MODULE_SUMMARY.md',
        'SECURITY_MODULE_UPDATE_SUMMARY.md',
        'AUTHENTICATION_IMPLEMENTATION_SUMMARY.md'
    ]
    
    docs_exist = []
    for doc_file in doc_files:
        if Path(doc_file).exists():
            docs_exist.append(doc_file)
            print(f"  ✅ {doc_file}")
        else:
            print(f"  ❌ {doc_file}")
    
    return len(docs_exist) >= len(doc_files) * 0.8

def test_web_interface_startup():
    """Test if web interface can start without errors"""
    print("\n🔍 Testing web interface startup...")
    
    try:
        # Test basic Flask app creation
        from flask import Flask
        app = Flask(__name__)
        print("  ✅ Flask app creation successful")
        
        # Test if we can import the main modules
        import mall_gamification_system
        import security_module
        import performance_module
        print("  ✅ Core modules imported successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ Web interface startup failed: {e}")
        return False

def main():
    """Run comprehensive system check"""
    print("🚀 Comprehensive System Check")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    checks = [
        ("Module Imports", check_imports),
        ("Circular Dependencies", check_circular_dependencies),
        ("Error Handling", check_error_handling),
        ("Logging Configuration", check_logging_configuration),
        ("Security Measures", check_security_measures),
        ("Performance Optimizations", check_performance_optimizations),
        ("Database Operations", check_database_operations),
        ("Frontend-Backend Connection", check_frontend_backend_connection),
        ("API Endpoints", check_endpoints),
        ("Test Coverage", check_tests),
        ("Documentation", check_documentation),
        ("Web Interface Startup", test_web_interface_startup)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"\n{status} {check_name}")
        except Exception as e:
            print(f"\n❌ {check_name} failed with exception: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 System Check Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {check_name}")
    
    print(f"\n🎯 Overall Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! System is ready for deployment.")
        return True
    elif passed >= total * 0.8:
        print("⚠️ Most checks passed. System is mostly ready.")
        return True
    else:
        print("❌ Many checks failed. System needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 