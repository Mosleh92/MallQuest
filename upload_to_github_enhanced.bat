@echo off
chcp 65001 >nul
echo 🚀 بدء رفع مشروع MallQuest إلى GitHub...
echo.

echo 📁 الانتقال إلى مجلد المشروع...
cd /d G:\Mosleh\g
if errorlevel 1 (
    echo ❌ خطأ: لا يمكن الوصول إلى مجلد المشروع
    pause
    exit /b 1
)

echo 🔍 التحقق من وجود Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Git غير مثبت
    echo 📥 يرجى تحميل Git من: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git مثبت بنجاح

echo 🔧 تهيئة Git...
if exist .git (
    echo ℹ️ Git موجود بالفعل
) else (
    git init
    if errorlevel 1 (
        echo ❌ خطأ في تهيئة Git
        pause
        exit /b 1
    )
)

echo 📝 إضافة جميع الملفات...
git add .
if errorlevel 1 (
    echo ❌ خطأ في إضافة الملفات
    pause
    exit /b 1
)

echo 💾 عمل Commit...
git commit -m "🎉 MallQuest: Complete Deerfields Mall Gamification System with Deer Care, Empire Management, and Notification Systems"
if errorlevel 1 (
    echo ❌ خطأ في عمل Commit
    echo ℹ️ قد تكون الملفات مضافة بالفعل
)

echo 🔗 ربط GitHub...
git remote add origin https://github.com/Mosleh92/MallQuest.git
if errorlevel 1 (
    echo ℹ️ المستودع البعيد موجود بالفعل
    git remote set-url origin https://github.com/Mosleh92/MallQuest.git
)

echo 🌿 تعيين الفرع الرئيسي...
git branch -M main

echo 📤 رفع المشروع...
echo ℹ️ قد يطلب منك إدخال اسم المستخدم وكلمة المرور
git push -u origin main
if errorlevel 1 (
    echo ❌ خطأ في رفع المشروع
    echo ℹ️ تأكد من:
    echo   1. اتصال الإنترنت
    echo   2. صحة بيانات GitHub
    echo   3. Personal Access Token
    pause
    exit /b 1
)

echo.
echo 🎉 تم رفع المشروع بنجاح!
echo 🌐 يمكنك مشاهدة المشروع على: https://github.com/Mosleh92/MallQuest
echo.
echo 📋 الملفات المرفوعة:
echo   ✅ deer_care_system.py - نظام رعاية الغزلان
echo   ✅ empire_management_system.py - نظام إدارة الإمبراطورية
echo   ✅ notification_system.py - نظام الإشعارات
echo   ✅ mall_gamification_system.py - النظام الأساسي
echo   ✅ web_interface.py - تطبيق Flask
echo   ✅ database.py - قاعدة البيانات
echo   ✅ README.md - الوثائق
echo   ✅ جميع الملفات الأخرى
echo.
pause 