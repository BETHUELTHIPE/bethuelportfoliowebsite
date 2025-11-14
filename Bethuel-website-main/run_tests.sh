#!/bin/bash

echo "🧪 Running Complete Production Test Suite"
echo "========================================"

# Make scripts executable
chmod +x test_services.sh
chmod +x deploy-full-stack.sh

# Install Python dependencies for testing
echo "📦 Installing test dependencies..."
pip install requests redis psycopg2-binary

echo ""
echo "🏥 Step 1: Health Check"
echo "----------------------"
python health_check.py

echo ""
echo "🔍 Step 2: Service Tests"
echo "----------------------"
./test_services.sh

echo ""
echo "🧪 Step 3: Functionality Tests"
echo "-----------------------------"
python test_production.py

echo ""
echo "📊 Step 4: Performance Check"
echo "---------------------------"
echo "Testing response times..."

# Test multiple endpoints for performance
endpoints=("/" "/about/" "/projects/" "/contact/" "/login/")

for endpoint in "${endpoints[@]}"; do
    echo -n "Testing $endpoint: "
    time=$(curl -o /dev/null -s -w "%{time_total}" http://localhost$endpoint)
    if (( $(echo "$time < 2.0" | bc -l) )); then
        echo "✅ ${time}s"
    else
        echo "⚠️  ${time}s (slow)"
    fi
done

echo ""
echo "🔐 Step 5: Security Check"
echo "------------------------"
echo "Checking security headers..."

# Check security headers
curl -I http://localhost | grep -E "(X-Frame-Options|X-Content-Type-Options|X-XSS-Protection)" || echo "⚠️  Some security headers missing"

echo ""
echo "📱 Step 6: Mobile Responsiveness"
echo "-------------------------------"
echo "Testing mobile user agent..."

mobile_response=$(curl -s -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)" http://localhost)
if echo "$mobile_response" | grep -q "viewport"; then
    echo "✅ Mobile viewport configured"
else
    echo "⚠️  Mobile viewport not found"
fi

echo ""
echo "🎯 Step 7: Feature Verification"
echo "------------------------------"

# Test specific features
echo "Testing authentication pages..."
auth_pages=("/login/" "/register/" "/password-reset/")

for page in "${auth_pages[@]}"; do
    status=$(curl -o /dev/null -s -w "%{http_code}" http://localhost$page)
    if [ "$status" = "200" ]; then
        echo "✅ $page accessible"
    else
        echo "❌ $page returned $status"
    fi
done

echo ""
echo "🏁 Test Suite Complete!"
echo "======================"

# Final summary
echo "✅ All tests completed. Check results above."
echo "🌐 Website: http://localhost"
echo "🔧 pgAdmin: http://localhost:5050"
echo "📊 Monitor with: docker-compose logs -f"