"""Kết nối XML-RPC tới hệ thống demo để bơm dữ liệu cho clip.

Mọi thông tin đăng nhập đọc từ biến môi trường, KHÔNG ghi vào tệp:
  VIINDOO_DEMO_URL        ví dụ https://sanxuat18.viindoo.cloud
  VIINDOO_DEMO_DB         tên cơ sở dữ liệu
  VIINDOO_DEMO_LOGIN      tài khoản quản trị demo
  VIINDOO_DEMO_PASSWORD   mật khẩu

Chạy thử:  python3 conn.py   -> in uid + danh sách công ty
"""
import os
import ssl
import xmlrpc.client


def _env(k):
    v = os.environ.get(k)
    if not v:
        raise SystemExit(f"thiếu biến môi trường {k} (hỏi người quản lý hệ thống demo)")
    return v


URL = os.environ.get("VIINDOO_DEMO_URL", "https://sanxuat18.viindoo.cloud")
DB, USER, PWD = _env("VIINDOO_DEMO_DB"), _env("VIINDOO_DEMO_LOGIN"), _env("VIINDOO_DEMO_PASSWORD")
ctx = ssl.create_default_context()
_common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common", context=ctx, allow_none=True)
_models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object", context=ctx, allow_none=True)
UID = _common.authenticate(DB, USER, PWD, {})


def call(model, method, args=None, kw=None):
    return _models.execute_kw(DB, UID, PWD, model, method, args or [], kw or {})


if __name__ == "__main__":
    print("uid:", UID)
    for c in call("res.company", "search_read", [[]], {"fields": ["id", "name"]}):
        print(c["id"], "|", c["name"])
