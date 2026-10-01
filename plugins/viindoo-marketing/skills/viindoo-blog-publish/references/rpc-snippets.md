# Đoạn mã JSON-RPC dùng lại (chạy trong trang viindoo.com bằng chrome-devtools `evaluate_script`)

Mọi đoạn mã đều cần hàm `call` ở mục 1 dán ở đầu. Nhớ đặt `waitForStableDom: false` cho các lệnh chỉ gọi RPC.

## Mục lục
1. Hàm gọi RPC
2. Nạp file từ máy (ảnh, JSON)
3. Upload ảnh thành attachment công khai
4. Tạo bài EN
5. Chạy Auto Translate
6. Ghi đè bản VI (nội dung + meta)
7. Đặt ảnh bìa
8. Kiểm tra

## 1. Hàm gọi RPC

```js
const call = async (model, method, args, kwargs = {}) => {
  const r = await fetch(`/web/dataset/call_kw/${model}/${method}`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({jsonrpc: '2.0', method: 'call', params: {model, method, args, kwargs}})});
  const j = await r.json();
  if (j.error) throw new Error(j.error.data ? j.error.data.message : j.error.message);
  return j.result;
};
const plain = h => { const d = document.createElement('div'); d.innerHTML = h; return d.textContent.replace(/\s+/g, ' ').trim(); };
```

## 2. Nạp file từ máy

Bước 1, `evaluate_script`: `() => { document.body.innerHTML = '<input type="file" id="up" multiple aria-label="upload">'; return 'ok'; }`
(Làm trên một tab phụ, vì thao tác này xoá nội dung trang.)
Bước 2, `take_snapshot` để lấy uid của nút upload, rồi `upload_file` với danh sách đường dẫn trong `~/Downloads`.
Bước 3, đọc file:

```js
const files = [...document.getElementById('up').files];
const readJSON = f => new Promise(res => { const r = new FileReader(); r.onload = () => res(JSON.parse(r.result)); r.readAsText(f); });
const readB64 = f => new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result.split(',')[1]); r.readAsDataURL(f); });
```

Nén ảnh trước khi upload: `sips -s format jpeg -s formatOptions 82 --resampleWidth 1600 in.png --out ~/Downloads/<ten-khong-dau>.jpg`. Ảnh bìa dùng 1920px.

## 3. Upload ảnh

```js
const out = [];
for (const f of files) {
  const id = await call('ir.attachment', 'create', [{name: f.name, datas: await readB64(f), mimetype: f.type || 'image/jpeg', public: true, res_model: 'ir.ui.view', res_id: 0}]);
  const [rec] = await call('ir.attachment', 'read', [[id], ['checksum']]);
  out.push({name: f.name, url: `/web/image/${id}-${rec.checksum.slice(0, 8)}/${encodeURIComponent(f.name)}`});
}
return out;
```

## 4. Tạo bài EN

Dùng file `create_values.json` do `build_post.py` sinh ra (nạp qua mục 2, không dán thẳng):

```js
const values = await readJSON(files.find(f => f.name.endsWith('create_values.json')));
const id = await call('blog.post', 'create', [values], {context: {lang: 'en_US'}});
const [p] = await call('blog.post', 'read', [[id], ['website_url']], {context: {lang: 'en_US'}});
return {id, url: p.website_url};
```

## 5. Chạy Auto Translate

Đây đúng là lệnh mà nút Action > Auto translate gọi, mất khoảng 35 giây.

```js
await call('wizard.confirm.auto.translate', 'action_confirm', [[POST_ID]], {context: {model: 'blog.post', record_ids: [POST_ID]}});
```

## 6. Ghi đè bản VI

`vi_map.json` là danh sách các cặp `[en_html, vi_html]`; `src_map` là object `{src_en: src_vi}` cho ảnh riêng theo ngôn ngữ; `meta.json` là `{field: [en, vi]}`.

```js
const map = await readJSON(files.find(f => f.name.endsWith('vi_map.json')));
const meta = await readJSON(files.find(f => f.name.endsWith('meta.json')));
const srcMap = map.src_map || {};
const pairs = map.terms || map;
const lookup = new Map(pairs.map(([en, vi]) => [plain(en), vi]));
const [tr] = await call('blog.post', 'get_field_translations', [[POST_ID], 'content'], {langs: ['vi_VN']});
const upd = {}, unmatched = [];
for (const t of tr) {
  const key = t.value || t.source;            // BẪY Odoo 17: khóa là đoạn VI hiện tại
  if (srcMap[t.source]) { upd[key] = srcMap[t.source]; continue; }
  if (/^\/|^https?:/.test(t.source)) continue; // link, ảnh không đổi
  let vi = lookup.get(plain(t.source));
  if (!vi) { unmatched.push(t.source.slice(0, 80)); continue; }
  const m = t.source.match(/^<(strong|em|b)>([\s\S]*)<\/\1>$/);
  if (m && !vi.startsWith(`<${m[1]}>`)) vi = `<${m[1]}>${vi}</${m[1]}>`;
  upd[key] = vi;
}
await call('blog.post', 'update_field_translations', [[POST_ID], 'content', {vi_VN: upd}]);
for (const f of ['name', 'subtitle', 'website_meta_title', 'website_meta_description', 'website_meta_keywords', 'seo_name'])
  if (meta[f]) await call('blog.post', 'update_field_translations', [[POST_ID], f, {vi_VN: meta[f][1]}]);
return {sent: Object.keys(upd).length, total: tr.length, unmatched};
```

`unmatched` thường là alt ảnh và nút CTA; thêm các cặp đó vào bảng đối chiếu (CTA: "Bắt đầu chuyển đổi doanh nghiệp của bạn" / "Bắt đầu ngay" / "Đặt lịch tư vấn") rồi chạy lại cho tới khi rỗng.

## 7. Đặt ảnh bìa

```js
const cover = JSON.stringify({'background-image': `url(${COVER_URL})`, 'background_color_class': 'o_cc3 o_cc', 'background_color_style': '', 'opacity': '0.6', 'resize_class': 'o_half_screen_height o_record_has_cover', 'text_align_class': ''});
await call('blog.post', 'write', [[POST_ID], {cover_properties: cover}], {context: {lang: 'en_US'}});
```

## 8. Kiểm tra

```js
const [tr] = await call('blog.post', 'get_field_translations', [[POST_ID], 'content'], {langs: ['vi_VN']});
const stillMachine = tr.filter(t => !/^\/|^https?:/.test(t.source) && lookup.has(plain(t.source)) && plain(t.value) !== plain(lookup.get(plain(t.source)))).length;
const empty = tr.filter(t => !/^\/|^https?:/.test(t.source) && !t.value && /[a-z]{4}/i.test(plain(t.source))).map(t => t.source.slice(0, 60));
const [en] = await call('blog.post', 'read', [[POST_ID], ['content']], {context: {lang: 'en_US'}});
const etxt = plain(en.content);
return {stillMachine, empty,
  viInEN: /[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]/i.test(etxt),
  longDash: /[---]/.test(etxt)};
```

Sau đó mở trang thật `https://viindoo.com/en/<website_url>` và `https://viindoo.com/vi/...`. Trên trang, kiểm tra `img.complete && img.naturalWidth > 0` sau khi cuộn tới (ảnh tải lười), rồi chụp màn hình phần đầu bài.
