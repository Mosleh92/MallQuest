@echo off
chcp 65001 >nul
title 🚀 رفع مشروع MallQuest إلى GitHub

echo.
echo ========================================
echo 🚀 بدء رفع مشروع MallQuest إلى GitHub
echo ========================================
echo.

echo 📁 الانتقال إلى مجلد المشروع...
cd /d G:\Mosleh\g
if errorlevel 1 (
    echo ❌ خطأ: لا يمكن الوصول إلى مجلد المشروع
    echo يرجى التأكد من وجود المجلد: G:\Mosleh\g
    pause
    exit /b 1
)
echo ✅ تم الانتقال إلى مجلد المشروع

echo.
echo 🔍 التحقق من وجود Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Git غير مثبت
    echo.
    echo 📥 يرجى تحميل Git من: https://git-scm.com/downloads
    echo أو تثبيت عبر Chocolatey: choco install git
    echo.
    pause
    exit /b 1
)
echo ✅ Git مثبت بنجاح

echo.
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
    echo ✅ تم تهيئة Git
)

echo.
echo 📝 إضافة جميع الملفات...
git add .
if errorlevel 1 (
    echo ❌ خطأ في إضافة الملفات
    pause
    exit /b 1
)
echo ✅ تم إضافة جميع الملفات

echo.
echo 💾 عمل Commit...
git commit -m "🎉 MallQuest: Complete Deerfields Mall Gamification System with Deer Care, Empire Management, and Notification Systems"
if errorlevel 1 (
    echo ℹ️ قد تكون الملفات مضافة بالفعل أو لا توجد تغييرات
    echo المتابعة...
)

echo.
echo 🔗 ربط GitHub...
git remote add origin https://github.com/Mosleh92/MallQuest.git
if errorlevel 1 (
    echo ℹ️ المستودع البعيد موجود بالفعل
    git remote set-url origin https://github.com/Mosleh92/MallQuest.git
    echo ✅ تم تحديث رابط المستودع
) else (
    echo ✅ تم ربط GitHub
)

echo.
echo 🌿 تعيين الفرع الرئيسي...
git branch -M main
echo ✅ تم تعيين الفرع الرئيسي

echo.
echo ========================================
echo 📤 رفع المشروع إلى GitHub...
echo ========================================
echo.
echo ℹ️ قد يطلب منك إدخال بيانات GitHub:
echo    Username: Mosleh92
echo    Password: Personal Access Token
echo.
echo 📋 إذا لم يكن لديك Personal Access Token:
echo    1. اذهب إلى: https://github.com/settings/tokens
echo    2. Generate new token (classic)
echo    3. اختر صلاحيات: repo, workflow
echo    4. انسخ الـ Token واستخدمه ككلمة مرور
echo.

git push -u origin main
if errorlevel 1 (
    echo.
    echo ❌ خطأ في رفع المشروع
    echo.
    echo 🔧 حلول محتملة:
    echo   1. تأكد من اتصال الإنترنت
    echo   2. تأكد من صحة بيانات GitHub
    echo   3. تأكد من Personal Access Token
    echo   4. تأكد من صلاحيات المستودع
    echo.
    echo 📞 للمساعدة، راجع ملف: GITHUB_TOKEN_SETUP.md
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 تم رفع المشروع بنجاح!
echo ========================================
echo.
echo 🌐 يمكنك مشاهدة المشروع على:
echo    https://github.com/Mosleh92/MallQuest
echo.
echo 📋 الملفات المرفوعة:
echo   ✅ deer_care_system.py - نظام رعاية الغزلان
echo   ✅ empire_management_system.py - نظام إدارة الإمبراطورية
echo   ✅ notification_system.py - نظام الإشعارات
echo   ✅ mall_gamification_system.py - النظام الأساسي
echo   ✅ web_interface.py - تطبيق Flask
echo   ✅ database.py - قاعدة البيانات المحسنة
echo   ✅ README.md - الوثائق الرئيسية
echo   ✅ جميع ملفات الوثائق والاختبارات
echo.
echo 🎊 مشروع MallQuest الآن على GitHub!
echo.
pause 