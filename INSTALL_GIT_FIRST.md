# 📥 تثبيت Git أولاً - ثم رفع المشروع

## 🎯 المشكلة
Git غير مثبت على نظامك. نحتاج لتثبيته أولاً.

## ⚡ طرق تثبيت Git

### الطريقة 1: التحميل المباشر (الأسهل)
1. **اذهب إلى**: https://git-scm.com/downloads
2. **اختر Windows**
3. **حمل أحدث إصدار**
4. **شغل الملف المحمل**
5. **اتبع خطوات التثبيت** (اضغط Next في كل خطوة)

### الطريقة 2: تثبيت عبر Chocolatey
```bash
# إذا كان لديك Chocolatey مثبت
choco install git
```

### الطريقة 3: تثبيت عبر Winget
```bash
# إذا كان لديك Winget
winget install --id Git.Git -e --source winget
```

## 🔍 التحقق من التثبيت

بعد التثبيت، افتح Command Prompt جديد ونفذ:
```bash
git --version
```

يجب أن تظهر رسالة مثل:
```
git version 2.40.0.windows.1
```

## 🚀 بعد تثبيت Git

### الطريقة 1: ملف Batch المحسن
```bash
# انقر نقراً مزدوجاً على:
UPLOAD_NOW.bat
```

### الطريقة 2: الأوامر اليدوية
```bash
cd G:\Mosleh\g
git init
git add .
git commit -m "MallQuest: Complete Deerfields Mall Gamification System"
git remote add origin https://github.com/Mosleh92/MallQuest.git
git branch -M main
git push -u origin main
```

## 🔑 Personal Access Token

إذا طلب منك GitHub كلمة مرور:
1. اذهب إلى: https://github.com/settings/tokens
2. Generate new token (classic)
3. اختر صلاحيات: `repo`, `workflow`
4. انسخ الـ Token واستخدمه ككلمة مرور

## 📁 الملفات التي سيتم رفعها

✅ **الأنظمة الجديدة:**
- `deer_care_system.py` - نظام رعاية الغزلان
- `empire_management_system.py` - نظام إدارة الإمبراطورية
- `notification_system.py` - نظام الإشعارات

✅ **الملفات الأساسية:**
- `mall_gamification_system.py` - النظام الأساسي
- `web_interface.py` - تطبيق Flask
- `database.py` - قاعدة البيانات
- `README.md` - الوثائق

## 🎉 النتيجة

بعد تثبيت Git ورفع المشروع، ستجد مشروعك على:
**https://github.com/Mosleh92/MallQuest**

## 🔧 إذا واجهت مشاكل

1. **أعد تشغيل Command Prompt** بعد تثبيت Git
2. **تأكد من تثبيت Git**: `git --version`
3. **تحقق من الإنترنت**: تأكد من الوصول لـ GitHub
4. **تحقق من الـ Token**: تأكد من صحة Personal Access Token

---

**🎊 أولاً: ثبت Git، ثم ارفع المشروع! 🌟** 