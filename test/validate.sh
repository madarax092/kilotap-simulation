#!/bin/bash
# KiloTap Simulation — Pre-push Validation Script
# Run before every commit to catch common errors

set -e
FILE="index.html"
FAILURES=0

echo "=== KiloTap Simulation Validator ==="
echo ""

# 1. File exists and has content
echo -n "[1] File present: "
if [ -f "$FILE" ] && [ -s "$FILE" ]; then
  SIZE=$(wc -c < "$FILE")
  echo "OK ($SIZE bytes)"
else
  echo "FAIL"
  FAILURES=$((FAILURES+1))
fi

# 2. Valid HTML structure
echo -n "[2] HTML structure: "
if grep -q '<!DOCTYPE html>' "$FILE" && grep -q '</html>' "$FILE"; then
  echo "OK"
else
  echo "FAIL — missing DOCTYPE or closing html tag"
  FAILURES=$((FAILURES+1))
fi

# 3. No double closing script tags (syntax error)
echo -n "[3] No double </script>: "
COUNT=$(grep -c '</script></script>' "$FILE" || true)
if [ "$COUNT" -eq 0 ]; then
  echo "OK"
else
  echo "FAIL — found $COUNT double </script> tags"
  FAILURES=$((FAILURES+1))
fi

# 4. Leaflet JS loaded (no Google Maps remnants)
echo -n "[4] Leaflet present: "
if grep -q 'leaflet.js' "$FILE"; then
  echo "OK"
else
  echo "FAIL — leaflet.js not found"
  FAILURES=$((FAILURES+1))
fi

# 5. No Google Maps references
echo -n "[5] No Google Maps: "
if grep -q 'maps.googleapis.com' "$FILE"; then
  echo "FAIL — Google Maps reference found"
  FAILURES=$((FAILURES+1))
else
  echo "OK"
fi

# 6. bgImageData null guard present
echo -n "[6] bgImageData null guard: "
if grep -q 'if (!bgImageData) return' "$FILE"; then
  echo "OK"
else
  echo "FAIL — null guard missing"
  FAILURES=$((FAILURES+1))
fi

# 7. COCO-SSD model loaded
echo -n "[7] COCO-SSD CDN: "
if grep -q 'coco-ssd' "$FILE"; then
  echo "OK"
else
  echo "FAIL — COCO-SSD not found"
  FAILURES=$((FAILURES+1))
fi

# 8. Photo data embedded
echo -n "[8] Photo base64: "
if grep -q 'data:image/jpeg;base64,' "$FILE"; then
  echo "OK"
else
  echo "FAIL — photo not embedded"
  FAILURES=$((FAILURES+1))
fi

# 9. No IMGBASE64 placeholder
echo -n "[9] No IMGBASE64 placeholder: "
if grep -q 'IMGBASE64' "$FILE"; then
  echo "FAIL — placeholder not replaced"
  FAILURES=$((FAILURES+1))
else
  echo "OK"
fi

# 10. Architecture: updateAll is YOLO-only (no map refs)
echo -n "[10] updateAll decoupled: "
UA_BODY=$(grep -A 5 'function updateAll()' "$FILE" | grep -v 'function updateAll')
if echo "$UA_BODY" | grep -q 'updateMapFilter\|typeof map'; then
  echo "FAIL — updateAll references map"
  FAILURES=$((FAILURES+1))
else
  echo "OK"
fi

# 11. PH_JUNK present (Philippine classification)
echo -n "[11] PH_JUNK labels: "
if grep -q 'PH_JUNK' "$FILE" && grep -q 'classifyPhilippine' "$FILE"; then
  echo "OK"
else
  echo "FAIL"
  FAILURES=$((FAILURES+1))
fi

# 12. No old JUNK_LABELS
echo -n "[12] No old JUNK_LABELS: "
if grep -q 'JUNK_LABELS' "$FILE"; then
  echo "FAIL — old JUNK_LABELS still present"
  FAILURES=$((FAILURES+1))
else
  echo "OK"
fi

# 13. HTTP server test — does curl get a 200?
echo -n "[13] HTTP server reachable: "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ | grep -q '200'; then
  echo "OK"
else
  echo "SKIP — server not running"
fi

# 14. JavaScript syntax check with Node
echo -n "[14] JavaScript syntax: "
# Extract JS between <script> tags, skipping external CDN scripts
python3 -c "
import re
with open('$FILE') as f:
    html = f.read()
# Extract inline script blocks
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
js = '\n'.join(scripts)
# Remove HTML comments that may confuse Node
js = re.sub(r'<!--.*?-->', '', js, flags=re.DOTALL)
with open('/tmp/_validate.js', 'w') as f:
    f.write(js)
" 2>/dev/null

if node --check /tmp/_validate.js 2>/tmp/_validate_err.txt; then
  echo "OK"
else
  echo "FAIL"
  cat /tmp/_validate_err.txt
  FAILURES=$((FAILURES+1))
fi

echo ""
echo "========================================="
if [ "$FAILURES" -eq 0 ]; then
  echo "ALL CHECKS PASSED — safe to push"
  exit 0
else
  echo "$FAILURES CHECK(S) FAILED — fix before pushing"
  exit 1
fi
