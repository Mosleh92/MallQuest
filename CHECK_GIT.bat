@echo off
echo ========================================
echo 🔍 التحقق من تثبيت Git
echo ========================================
echo.

git --version
if errorlevel 1 (
    echo.
    echo ❌ Git غير مثبت!
    echo.
    echo 📥 يرجى تثبيت Git من:
    echo    https://git-scm.com/downloads
    echo.
    echo 📋 خطوات التثبيت:
    echo    1. اذهب إلى الرابط أعلاه
    echo    2. اختر Windows
    echo    3. حمل أحدث إصدار
    echo    4. شغل الملف المحمل
    echo    5. اتبع خطوات التثبيت
    echo.
    echo 🔄 بعد التثبيت، أعد تشغيل هذا الملف
    echo.
) else (
    echo.
    echo ✅ Git مثبت بنجاح!
    echo.
    echo 🚀 يمكنك الآن رفع المشروع:
    echo    انقر على UPLOAD_NOW.bat
    echo.
)

pause 