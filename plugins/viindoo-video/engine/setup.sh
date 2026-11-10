#!/bin/bash
# Cai thu vien cho engine (gsap, puppeteer-core) vao thu muc lam viec cua nguoi dung,
# KHONG cai vao thu muc plugin (thu muc plugin bi thay moi khi cap nhat plugin).
#
# Chay:  bash "${CLAUDE_PLUGIN_ROOT}/engine/setup.sh"
# Dich:  ${VIINDOO_VIDEO_WORKDIR:-~/viindoo-video}/.engine-deps/node_modules
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORKDIR="${VIINDOO_VIDEO_WORKDIR:-$HOME/viindoo-video}"
DEPS="$WORKDIR/.engine-deps"

command -v node >/dev/null || { echo "Can Node.js 18 tro len (brew install node)"; exit 1; }
command -v ffmpeg >/dev/null || echo "Canh bao: chua co ffmpeg (brew install ffmpeg) - render se loi o buoc xuat."

mkdir -p "$DEPS"
cp "$HERE/package.json" "$HERE/package-lock.json" "$DEPS/"
( cd "$DEPS" && npm ci --no-audit --no-fund )
echo "Da cai thu vien engine vao $DEPS/node_modules"
echo "Thu render: node \"$HERE/sequence.mjs\" --seq \"$HERE/samples/seq-mau.json\""
