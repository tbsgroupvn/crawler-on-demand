@echo off
echo 🚀 Pushing Crawler On Demand to GitHub...
echo.
echo ⚠️  Make sure you have created the repository on GitHub first!
echo    Repository name: crawler-on-demand
echo    URL should be: https://github.com/YOUR_USERNAME/crawler-on-demand.git
echo.
echo 📝 Please replace YOUR_USERNAME with your GitHub username in the command below:
echo.

REM Replace YOUR_USERNAME with your actual GitHub username
set /p username="Enter your GitHub username: "

echo.
echo 🔗 Adding remote origin...
git remote add origin https://github.com/%username%/crawler-on-demand.git

echo.
echo 📤 Pushing to GitHub...
git push -u origin main

echo.
echo ✅ Done! Your project is now on GitHub at:
echo    https://github.com/%username%/crawler-on-demand
echo.
echo 🌟 Don't forget to:
echo    - Add a star to your own repository ⭐
echo    - Share it with friends and colleagues
echo    - Update the README.md with your GitHub username
echo.
pause 