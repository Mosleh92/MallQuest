#!/usr/bin/env python3
"""
Test Import Fix
Tests if the mall_gamification_system.py import issue is resolved
"""

def test_import():
    """Test importing the main system"""
    try:
        import mall_gamification_system
        print("✅ تم استيراد mall_gamification_system بنجاح")
        
        # Test creating system instance
        system = mall_gamification_system.MallGamificationSystem()
        print("✅ تم إنشاء نظام Gamification بنجاح")
        
        # Test creating a user
        user = system.create_user("test_user", "en")
        print("✅ تم إنشاء مستخدم بنجاح")
        
        print("\n🎉 جميع الاختبارات نجحت! المشكلة تم حلها.")
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ آخر: {e}")
        return False

if __name__ == "__main__":
    print("🧪 اختبار إصلاح مشكلة الاستيراد")
    print("=" * 40)
    test_import() 