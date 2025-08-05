# 🚀 رفع مشروع MallQuest إلى GitHub
# تشغيل كمدير: PowerShell كمدير

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 بدء رفع مشروع MallQuest إلى GitHub" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# الانتقال إلى مجلد المشروع
Write-Host "📁 الانتقال إلى مجلد المشروع..." -ForegroundColor Yellow
try {
    Set-Location "G:\Mosleh\g"
    Write-Host "✅ تم الانتقال إلى مجلد المشروع" -ForegroundColor Green
} catch {
    Write-Host "❌ خطأ: لا يمكن الوصول إلى مجلد المشروع" -ForegroundColor Red
    Write-Host "يرجى التأكد من وجود المجلد: G:\Mosleh\g" -ForegroundColor Yellow
    Read-Host "اضغط Enter للخروج"
    exit 1
}

Write-Host ""

# التحقق من وجود Git
Write-Host "🔍 التحقق من وجود Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git مثبت بنجاح: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ خطأ: Git غير مثبت" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 يرجى تحميل Git من: https://git-scm.com/downloads" -ForegroundColor Yellow
    Write-Host "أو تثبيت عبر Chocolatey: choco install git" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "اضغط Enter للخروج"
    exit 1
}

Write-Host ""

# تهيئة Git
Write-Host "🔧 تهيئة Git..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "ℹ️ Git موجود بالفعل" -ForegroundColor Blue
} else {
    try {
        git init
        Write-Host "✅ تم تهيئة Git" -ForegroundColor Green
    } catch {
        Write-Host "❌ خطأ في تهيئة Git" -ForegroundColor Red
        Read-Host "اضغط Enter للخروج"
        exit 1
    }
}

Write-Host ""

# إضافة الملفات
Write-Host "📝 إضافة جميع الملفات..." -ForegroundColor Yellow
try {
    git add .
    Write-Host "✅ تم إضافة جميع الملفات" -ForegroundColor Green
} catch {
    Write-Host "❌ خطأ في إضافة الملفات" -ForegroundColor Red
    Read-Host "اضغط Enter للخروج"
    exit 1
}

Write-Host ""

# عمل Commit
Write-Host "💾 عمل Commit..." -ForegroundColor Yellow
try {
    git commit -m "🎉 MallQuest: Complete Deerfields Mall Gamification System with Deer Care, Empire Management, and Notification Systems"
    Write-Host "✅ تم عمل Commit" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ قد تكون الملفات مضافة بالفعل أو لا توجد تغييرات" -ForegroundColor Blue
    Write-Host "المتابعة..." -ForegroundColor Blue
}

Write-Host ""

# ربط GitHub
Write-Host "🔗 ربط GitHub..." -ForegroundColor Yellow
try {
    git remote add origin https://github.com/Mosleh92/MallQuest.git
    Write-Host "✅ تم ربط GitHub" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ المستودع البعيد موجود بالفعل" -ForegroundColor Blue
    git remote set-url origin https://github.com/Mosleh92/MallQuest.git
    Write-Host "✅ تم تحديث رابط المستودع" -ForegroundColor Green
}

Write-Host ""

# تعيين الفرع الرئيسي
Write-Host "🌿 تعيين الفرع الرئيسي..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ تم تعيين الفرع الرئيسي" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📤 رفع المشروع إلى GitHub..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "ℹ️ قد يطلب منك إدخال بيانات GitHub:" -ForegroundColor Yellow
Write-Host "   Username: Mosleh92" -ForegroundColor White
Write-Host "   Password: Personal Access Token" -ForegroundColor White
Write-Host ""

Write-Host "📋 إذا لم يكن لديك Personal Access Token:" -ForegroundColor Yellow
Write-Host "   1. اذهب إلى: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "   2. Generate new token (classic)" -ForegroundColor White
Write-Host "   3. اختر صلاحيات: repo, workflow" -ForegroundColor White
Write-Host "   4. انسخ الـ Token واستخدمه ككلمة مرور" -ForegroundColor White
Write-Host ""

# رفع المشروع
try {
    git push -u origin main
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "🎉 تم رفع المشروع بنجاح!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌐 يمكنك مشاهدة المشروع على:" -ForegroundColor Cyan
    Write-Host "   https://github.com/Mosleh92/MallQuest" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 الملفات المرفوعة:" -ForegroundColor Yellow
    Write-Host "   ✅ deer_care_system.py - نظام رعاية الغزلان" -ForegroundColor Green
    Write-Host "   ✅ empire_management_system.py - نظام إدارة الإمبراطورية" -ForegroundColor Green
    Write-Host "   ✅ notification_system.py - نظام الإشعارات" -ForegroundColor Green
    Write-Host "   ✅ mall_gamification_system.py - النظام الأساسي" -ForegroundColor Green
    Write-Host "   ✅ web_interface.py - تطبيق Flask" -ForegroundColor Green
    Write-Host "   ✅ database.py - قاعدة البيانات المحسنة" -ForegroundColor Green
    Write-Host "   ✅ README.md - الوثائق الرئيسية" -ForegroundColor Green
    Write-Host "   ✅ جميع ملفات الوثائق والاختبارات" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎊 مشروع MallQuest الآن على GitHub!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "❌ خطأ في رفع المشروع" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 حلول محتملة:" -ForegroundColor Yellow
    Write-Host "   1. تأكد من اتصال الإنترنت" -ForegroundColor White
    Write-Host "   2. تأكد من صحة بيانات GitHub" -ForegroundColor White
    Write-Host "   3. تأكد من Personal Access Token" -ForegroundColor White
    Write-Host "   4. تأكد من صلاحيات المستودع" -ForegroundColor White
    Write-Host ""
    Write-Host "📞 للمساعدة، راجع ملف: GITHUB_TOKEN_SETUP.md" -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "اضغط Enter للخروج" 