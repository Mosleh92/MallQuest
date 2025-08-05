@echo off
echo رفع مشروع MallQuest إلى GitHub...
echo.

cd /d G:\Mosleh\g
git init
git add .
git commit -m "MallQuest: Complete Deerfields Mall Gamification System"
git remote add origin https://github.com/Mosleh92/MallQuest.git
git branch -M main
git push -u origin main

echo.
echo تم رفع المشروع!
pause 