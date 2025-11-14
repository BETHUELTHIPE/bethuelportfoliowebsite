@echo off
echo 🧪 Running Complete Production Test Suite
echo ========================================

echo 📦 Installing test dependencies...
pip install requests redis psycopg2-binary

echo.
echo 🏥 Step 1: Health Check
echo ----------------------
python health_check.py

echo.
echo 🧪 Step 2: Functionality Tests
echo -----------------------------
python test_production.py

echo.
echo 📊 Step 3: Docker Services Check
echo -------------------------------
docker-compose ps

echo.
echo 🌐 Step 4: Quick Endpoint Tests
echo ------------------------------
curl -s -o nul -w "Website Status: %%{http_code}" http://localhost
echo.
curl -s -o nul -w "pgAdmin Status: %%{http_code}" http://localhost:5050
echo.

echo.
echo 🏁 Test Suite Complete!
echo ======================
echo ✅ All tests completed. Check results above.
echo 🌐 Website: http://localhost
echo 🔧 pgAdmin: http://localhost:5050
pause