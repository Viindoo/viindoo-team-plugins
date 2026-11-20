# -*- coding: utf-8 -*-
"""Kết nối CHỈ ĐỌC tới hệ thống Viindoo/Odoo đang vận hành của khách qua JSON-RPC (phiên đăng nhập web).

Chỉ cho gọi các phương thức đọc trong READ_METHODS; mọi phương thức khác bị chặn ngay tại máy, không gửi lên máy chủ.
Thông tin đăng nhập lấy từ biến môi trường, không ghi vào tệp:
  ODOO_URL, ODOO_DB (khi máy chủ có nhiều cơ sở dữ liệu), ODOO_LOGIN, ODOO_PASSWORD
Nên dùng một tài khoản riêng cho Viindoo, không dùng tài khoản của người dùng khách.
"""
import http.cookiejar
import json
import os
import re
import urllib.parse
import urllib.request

READ_METHODS = {"search_read", "search_count", "read", "read_group", "fields_get", "name_search", "search"}


class ReadOnlyError(Exception):
    pass


class Client:
    def __init__(self, url=None, db=None, login=None, password=None, lang="vi_VN"):
        self.url = (url or os.environ.get("ODOO_URL") or "").rstrip("/")
        if not self.url:
            raise SystemExit("Thiếu ODOO_URL (địa chỉ hệ thống của khách)")
        self.db = db or os.environ.get("ODOO_DB")
        self.login = login or os.environ.get("ODOO_LOGIN")
        password = password or os.environ.get("ODOO_PASSWORD")
        if not (self.login and password):
            raise SystemExit("Thiếu ODOO_LOGIN / ODOO_PASSWORD (đặt trong biến môi trường, không ghi vào tệp)")
        self._op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self._authenticate(password)
        info = self._call("/web/session/get_session_info", {})
        self.lang = (info.get("user_context") or {}).get("lang") or "en_US"
        langs = [r["code"] for r in self._call("/web/dataset/call_kw", {"model": "res.lang", "method": "search_read",
                                                                          "args": [[("active", "=", True)]], "kwargs": {"fields": ["code"]}})]
        if lang in langs:
            self.lang = lang      # tên nhóm quyền, tên menu đọc đúng chữ tiếng Việt người dùng thấy
        else:
            print(f"Cảnh báo: hệ thống chưa bật ngôn ngữ {lang}; đọc theo {self.lang}")
        self.server_version = info.get("server_version", "")
        self.uid = info.get("uid")
        comp = (info.get("user_companies") or {}).get("allowed_companies") or {}
        self.companies = [int(c) for c in comp.keys()] or None
        self._fields = {}

    def _authenticate(self, password):
        if self.db:
            res = self._call("/web/session/authenticate", {"db": self.db, "login": self.login, "password": password})
            if not res or not res.get("uid"):
                raise SystemExit("Đăng nhập không thành công")
            return
        h = self._op.open(self.url + "/web/login", timeout=60).read().decode()
        tok = re.search(r'name="csrf_token" value="([^"]+)"', h)
        if not tok:
            raise SystemExit("Không đọc được trang đăng nhập; thử đặt ODOO_DB")
        self._op.open(self.url + "/web/login", urllib.parse.urlencode(
            {"csrf_token": tok.group(1), "login": self.login, "password": password, "redirect": ""}).encode(), timeout=60)

    def _call(self, path, params):
        req = urllib.request.Request(self.url + path, json.dumps({"jsonrpc": "2.0", "method": "call", "params": params}).encode(),
                                     {"Content-Type": "application/json"})
        d = json.loads(self._op.open(req, timeout=180).read())
        if d.get("error"):
            raise Exception(d["error"].get("data", {}).get("message") or json.dumps(d["error"])[:300])
        return d["result"]

    def kw(self, model, method, args=None, **kwargs):
        if method not in READ_METHODS:
            raise ReadOnlyError(f"Phương thức '{method}' không phải phương thức đọc - bị chặn")
        ctx = {"lang": self.lang, "active_test": True, **(kwargs.pop("context", None) or {})}
        if self.companies:
            ctx.setdefault("allowed_company_ids", self.companies)
        return self._call("/web/dataset/call_kw", {"model": model, "method": method, "args": args or [], "kwargs": {**kwargs, "context": ctx}})

    # ---------------------------------------------------------------- tiện ích
    def has_model(self, model):
        try:
            self.fields(model)
            return True
        except Exception:
            return False

    def fields(self, model):
        if model not in self._fields:
            self._fields[model] = self.kw(model, "fields_get", [], attributes=["type", "relation", "string"])
        return self._fields[model]

    def has_field(self, model, field):
        try:
            return field in self.fields(model)
        except Exception:
            return False

    def sr(self, model, domain=None, fields=None, limit=0, order=None, context=None):
        return self.kw(model, "search_read", [domain or []], fields=fields or ["display_name"], limit=limit, order=order, context=context)

    def count(self, model, domain=None, context=None):
        return self.kw(model, "search_count", [domain or []], context=context)

    def group(self, model, domain, fields, groupby, context=None):
        return self.kw(model, "read_group", [domain, fields, groupby], lazy=False, context=context)

    def xmlid(self, module, name):
        r = self.sr("ir.model.data", [("module", "=", module), ("name", "=", name)], ["res_id"], limit=1)
        return r[0]["res_id"] if r else None
