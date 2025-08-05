# 🚀 الدليل النهائي لرفع مشروع MallQuest

## 🎯 المشكلة الحالية
Git غير مثبت على نظامك. نحتاج لحل هذه المشكلة أولاً.

## 📥 الخطوة 1: تثبيت Git

### الطريقة الأسهل:
1. **اذهب إلى**: https://git-scm.com/downloads
2. **اختر Windows**
3. **حمل أحدث إصدار**
4. **شغل الملف المحمل**
5. **اتبع خطوات التثبيت** (اضغط Next في كل خطوة)

### أو استخدم ملف التحقق:
```bash
# انقر نقراً مزدوجاً على:
CHECK_GIT.bat
```

## 🔍 الخطوة 2: التحقق من التثبيت

بعد التثبيت، افتح Command Prompt جديد ونفذ:
```bash
git --version
```

يجب أن تظهر رسالة مثل:
```
git version 2.40.0.windows.1
```

## 🚀 الخطوة 3: رفع المشروع

### الطريقة الأسهل:
```bash
# انقر نقراً مزدوجاً على:
UPLOAD_NOW.bat
```

### أو الأوامر اليدوية:
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

✅ **جميع ملفات الوثائق والاختبارات**

## 🎉 النتيجة

بعد تثبيت Git ورفع المشروع، ستجد مشروعك على:
**https://github.com/Mosleh92/MallQuest**

## 📋 ملخص الخطوات

1. **ثبت Git** من https://git-scm.com/downloads
2. **تحقق من التثبيت** باستخدام `CHECK_GIT.bat`
3. **ارفع المشروع** باستخدام `UPLOAD_NOW.bat`
4. **استخدم Personal Access Token** عند الطلب

## 🔧 إذا واجهت مشاكل

1. **أعد تشغيل Command Prompt** بعد تثبيت Git
2. **تأكد من تثبيت Git**: `git --version`
3. **تحقق من الإنترنت**: تأكد من الوصول لـ GitHub
4. **تحقق من الـ Token**: تأكد من صحة Personal Access Token

---

**🎊 اتبع الخطوات بالترتيب وستنجح! 🌟** 