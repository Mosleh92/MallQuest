# 🚀 رفع مشروع MallQuest إلى GitHub
Write-Host "🚀 بدء رفع مشروع MallQuest إلى GitHub..." -ForegroundColor Green
Write-Host ""

# الانتقال إلى مجلد المشروع
Write-Host "📁 الانتقال إلى مجلد المشروع..." -ForegroundColor Yellow
Set-Location "G:\Mosleh\g"

# تهيئة Git
Write-Host "🔧 تهيئة Git..." -ForegroundColor Yellow
git init

# إضافة جميع الملفات
Write-Host "📝 إضافة جميع الملفات..." -ForegroundColor Yellow
git add .

# عمل Commit
Write-Host "💾 عمل Commit..." -ForegroundColor Yellow
git commit -m "🎉 MallQuest: Complete Deerfields Mall Gamification System with Deer Care, Empire Management, and Notification Systems"

# ربط GitHub
Write-Host "🔗 ربط GitHub..." -ForegroundColor Yellow
git remote add origin https://github.com/Mosleh92/MallQuest.git

# تعيين الفرع الرئيسي
Write-Host "🌿 تعيين الفرع الرئيسي..." -ForegroundColor Yellow
git branch -M main

# رفع المشروع
Write-Host "📤 رفع المشروع..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "🎉 تم رفع المشروع بنجاح!" -ForegroundColor Green
Write-Host "🌐 يمكنك مشاهدة المشروع على: https://github.com/Mosleh92/MallQuest" -ForegroundColor Cyan
Write-Host ""
Read-Host "اضغط Enter للخروج" 