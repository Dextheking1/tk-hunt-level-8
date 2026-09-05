#!/bin/sh
# PREREG_DICTIONARY_STEGHIDE.md — final dictionary sweep driver.
# Requires: steghide (or stegseek), the four residual carriers, the frozen wordlist.
set -u
WLIST="${1:-steghide_dictionary.txt}"
CARRIERS="image02.jpg image06.jpg image07.jpg image12.jpg"

echo "=== positive control: blank-password payload from image04.jpg ==="
mkdir -p /tmp/dsweep && cd /tmp/dsweep
if steghide extract -sf "$OLDPWD/image04.jpg" -p "" -f diag_out.jpg -x diag_out.jpg 2>/dev/null; then
  sha256sum diag_out.jpg
  echo "(expected 7643d7326d34fe2671a545f0443c2f0e40536c3ea450959103f90dc8771ac7a0)"
else
  echo "POSITIVE CONTROL FAILED — abort"
  exit 2
fi

echo "=== negative control: fresh flat JPEG ==="
python3 - <<'PY'
from PIL import Image
im = Image.new("RGB", (640, 480), (200, 120, 90))
im.save("flat_control.jpg", quality=90)
PY
steghide embed -sf flat_control.jpg -p "" -f diag_out.jpg -e flat_embed.jpg 2>/dev/null
steghide extract -sf flat_embed.jpg -p "zzz_not_the_pass" -f diag_out.jpg -x c1.jpg 2>/dev/null && echo "UNEXPECTED" || true

for c in $CARRIERS; do
  echo "=== $c ==="
  out=""; hit=""
  if command -v stegseek >/dev/null 2>&1; then
    stegseek "$OLDPWD/$c" -w "$WLIST" -o /tmp/dsweep/out_$(basename "$c" .jpg).bin \
      && hit="stegseek:VALIDATED" || hit="stegseek:no-passphrase"
  else
    while IFS= read -r pw; do
      if steghide extract -sf "$OLDPWD/$c" -p "$pw" -f /tmp/dsweep/out_$(basename "$c" .jpg).bin \
           -x /tmp/dsweep/out_$(basename "$c" .jpg).bin >/dev/null 2>&1; then
        # validate: stable second extraction
        if steghide extract -sf "$OLDPWD/$c" -p "$pw" -f /tmp/dsweep/out2.bin \
             -x /tmp/dsweep/out2.bin >/dev/null 2>&1 \
           && cmp -s /tmp/dsweep/out_$(basename "$c" .jpg).bin /tmp/dsweep/out2.bin; then
          hit="steghide:VALIDATED pw=$pw"; out=/tmp/dsweep/out_$(basename "$c" .jpg).bin
        fi
        break
      fi
    done < "$WLIST"
    [ -z "$hit" ] && hit="steghide:no-passphrase"
  fi
  echo "   -> $hit"
done
echo "=== done ==="
