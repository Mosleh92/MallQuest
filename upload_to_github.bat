@echo off
echo 🚀 بدء رفع مشروع MallQuest إلى GitHub...
echo.

echo 📁 الانتقال إلى مجلد المشروع...
cd /d G:\Mosleh\g

echo 🔧 تهيئة Git...
git init

echo 📝 إضافة جميع الملفات...
git add .

echo 💾 عمل Commit...
git commit -m "🎉 MallQuest: Complete Deerfields Mall Gamification System with Deer Care, Empire Management, and Notification Systems"

echo 🔗 ربط GitHub...
git remote add origin https://github.com/Mosleh92/MallQuest.git

echo 🌿 تعيين الفرع الرئيسي...
git branch -M main

echo 📤 رفع المشروع...
git push -u origin main

echo.
echo 🎉 تم رفع المشروع بنجاح!
echo 🌐 يمكنك مشاهدة المشروع على: https://github.com/Mosleh92/MallQuest
echo.
pause 