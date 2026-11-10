# VÍ DỤ THAM KHẢO (không chạy độc lập): kịch bản quay thao tác thật cho clip ra mắt Điều hành xưởng sản xuất trên instance demo.
# Dùng để học cách: làm trên bản sao lệnh + file trạng thái + dọn trong finally; ghi video từng cảnh (record_video), vòng chạm, cắt thời gian chết;
# đổi ngôn ngữ người dùng + tên hiển thị tạm cho bản EN rồi trả lại. Phụ thuộc approval_common.py / capture_shots.py của bộ clip cơ khí (không kèm).
# Thông tin đăng nhập lấy từ biến môi trường ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD.
"""Real screenshots + short screen videos of Shop Floor Control (viin_mrp_workorder) on the demo instance, company 4.
Run:  $VIDEO_PY capture.py vi|en   (python co playwright)
Output: ../sf_<lang>/assets/shots_real/<key>.png + <key>.mp4 + shots.json (Shooter format + video, video_w, video_h, duration).

Works on COPIES of manufacturing order QV/MO/00003 (8 stainless electrical cabinets, routing laser > bending > welding > QC):
  copy A drives the operator scenes on the laser cutting station, copy B (first 3 operations finished, 5/8 recorded)
  drives the close / consumption-difference scenes on the QC station. Every created record is listed in a state file and
  removed in a finally block; the next run first cleans what a crashed run left. Never confirms scrap, never closes an
  order, never changes a BOM; a station stopped by the script is restarted. EN pass: admin language en_US and the
  rollback-able English display names (../../demo-data/30_en_display_names.py), both restored at the end."""
import json, os, subprocess, sys, time, shutil, tempfile
from pathlib import Path

for k in ("ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_PASSWORD"):
    assert os.environ.get(k), f"thiếu biến môi trường {k}"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from approval_common import rpc, one, Shooter, new_page, B, CSS, EXTRA_CSS, NM   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402

LANG = sys.argv[1] if len(sys.argv) > 1 else ""
assert LANG in ("vi", "en"), "usage: capture.py vi|en"
DEMO = HERE.parent.parent.parent / "demo-data"
OUT = HERE.parent / f"sf_{LANG}" / "assets" / "shots_real"
STATE = HERE / f".created_{LANG}.json"
SRC_MO = "QV/MO/00003"            # TD-500-SUS, 8 units, 4 operations
WC_LASER, WC_MILL, WC_QC = 27, 26, 30
EMP_OTHER = 213                    # Le Minh Duc, credited in the On behalf scene
LOSS_SETUP = 3                     # "Setup and Adjustments" stop reason
PORTRAIT, LANDSCAPE = (800, 1280), (1280, 800)
T = {"vi": {"undone": "Đã hoàn tác", "behalf": "Thay mặt", "laser": "Cắt laser"},
     "en": {"undone": "Undone", "behalf": "On Behalf", "laser": "Laser Cutting"}}[LANG]

# tap indicator (ripple at each pointer-down) + the clean-screen CSS, injected in every page of every context
INIT_JS = """(() => {
  const css = %s;
  const add = () => {
    if (window.__sfTap) return; window.__sfTap = true;
    const st = document.createElement('style');
    st.textContent = css + `.__sf_tap{position:fixed;width:60px;height:60px;margin:-30px 0 0 -30px;border-radius:50%%;
      background:rgba(30,30,30,.40);border:2px solid rgba(255,255,255,.9);box-shadow:0 0 0 1px rgba(0,0,0,.25);
      pointer-events:none;z-index:2147483647;animation:__sf_tap_k .6s ease-out forwards}
      @keyframes __sf_tap_k{0%%{transform:scale(.45);opacity:1}100%%{transform:scale(1.35);opacity:0}}
      *{cursor:none!important}`;
    document.documentElement.appendChild(st);
    document.addEventListener('pointerdown', e => {
      const d = document.createElement('div'); d.className = '__sf_tap';
      d.style.left = e.clientX + 'px'; d.style.top = e.clientY + 'px';
      document.documentElement.appendChild(d); setTimeout(() => d.remove(), 650);
    }, true);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', add); else add();
})();""" % json.dumps(CSS + EXTRA_CSS)

SH = Shooter(OUT)
st = {"mos": [], "moves": [], "prod_baseline": None, "lang_changed": False, "en_applied": False}
videos = {}     # key -> (file, w, h, duration)
failed = []


def save_state():
    STATE.write_text(json.dumps(st))


def log_err(e):
    return str(e).strip().splitlines()[-1][:250]


# ---------------------------------------------------------------- data (copies) and cleanup
def copy_mo(src):
    mo = one(rpc("mrp.production", "copy", [src]))
    st["mos"].append(mo); save_state()
    rpc("mrp.production", "action_confirm", [mo])
    r = rpc("mrp.production", "read", [mo], ["name", "workorder_ids", "move_raw_ids", "move_finished_ids"])[0]
    st["moves"] += r["move_raw_ids"] + r["move_finished_ids"]; save_state()
    return mo, r["name"], r["workorder_ids"], r["move_raw_ids"]


def cleanup():
    """Restart a station stopped by us, then remove time lines, quality checks, activities, order copies and their moves."""
    mos = [m for m in st["mos"] if rpc("mrp.production", "search", [("id", "=", m)])]
    wos = rpc("mrp.workorder", "search", [("production_id", "in", mos)]) if mos else []
    for wc in (WC_LASER, WC_QC):
        if rpc("mrp.workcenter", "read", [wc], ["working_state"])[0]["working_state"] == "blocked":
            try:
                live = rpc("mrp.workorder", "search", [("id", "in", wos), ("workcenter_id", "=", wc), ("state", "in", ["ready", "progress"])])
                if live: rpc("mrp.workorder", "action_shopfloor_unblock", [live[0]])
                else: rpc("mrp.workcenter", "unblock", [wc])
                print("restarted work center", wc)
            except RuntimeError as e:
                print("COULD NOT RESTART work center", wc, log_err(e))
    base = st.get("prod_baseline")
    if base is not None:
        dom = [("id", ">", base), "|", ("workorder_id", "in", wos or [0]),
               "&", "&", ("workorder_id", "=", False), ("workcenter_id", "in", [WC_LASER, WC_QC]), ("create_uid", "=", 2)]
        lines = rpc("mrp.workcenter.productivity", "search", dom)
        if lines:
            try: rpc("mrp.workcenter.productivity", "unlink", lines); print("removed time lines", lines)
            except RuntimeError as e: print("COULD NOT REMOVE time lines", lines, log_err(e))
    if mos:
        for model, dom in (("viin.quality.check", [("production_id", "in", mos)]),
                           ("mail.activity", [("res_model", "=", "mrp.production"), ("res_id", "in", mos)])):
            ids = rpc(model, "search", dom)
            if ids:
                try: rpc(model, "unlink", ids); print("removed", model, ids)
                except RuntimeError as e: print("COULD NOT REMOVE", model, ids, log_err(e))
        try:
            rpc("mrp.production", "action_cancel", mos)
            if wos: rpc("mrp.workorder", "unlink", wos)    # shop floor entries cascade with their work order
            msgs = rpc("mail.message", "search", [("model", "=", "mrp.production"), ("res_id", "in", mos)])
            rpc("mrp.production", "unlink", mos); print("removed order copies", mos)
            if msgs:
                try: rpc("mail.message", "unlink", msgs)
                except RuntimeError: pass
        except RuntimeError as e:
            print("COULD NOT REMOVE order copies", mos, log_err(e))
    moves = rpc("stock.move", "search", [("id", "in", st["moves"]), ("state", "=", "cancel")]) if st["moves"] else []
    extra = rpc("stock.move", "search", [("raw_material_production_id", "in", mos)]) if mos else []
    if moves:
        try: rpc("stock.move", "unlink", moves)
        except RuntimeError as e: print("COULD NOT REMOVE moves", moves, log_err(e))
    left = {"mrp.production": rpc("mrp.production", "search", [("id", "in", st["mos"])]),
            "stock.move": rpc("stock.move", "search", [("id", "in", st["moves"] + extra)]) if st["moves"] or extra else [],
            "blocked work centers": rpc("mrp.workcenter", "search", [("id", "in", [WC_LASER, WC_QC]), ("working_state", "=", "blocked")])}
    return {k: v for k, v in left.items() if v}


def en_names(rollback=False):
    cmd = ["python3", str(DEMO / "30_en_display_names.py")] + (["--rollback"] if rollback else [])
    p = subprocess.run(cmd, cwd=str(DEMO), capture_output=True, text=True, env=os.environ)
    print(p.stdout.strip()[-400:])
    if p.returncode: raise RuntimeError("30_en_display_names failed: " + p.stderr[-600:])


def restore_env():
    if st.get("lang_changed"):
        rpc("res.users", "write", [2], {"lang": "vi_VN"}); st["lang_changed"] = False; save_state(); print("admin language back to vi_VN")
    if st.get("en_applied") or (DEMO / "30_en_display_names.rollback.json").exists():
        en_names(rollback=True); st["en_applied"] = False; save_state()


# ---------------------------------------------------------------- browser helpers
class Scene:
    """One recorded browser context per scene. Navigation before start() and the tail after stop() are trimmed off."""
    def __init__(self, br, storage, key, viewport):
        self.key, self.vp = key, viewport
        self.dir = tempfile.mkdtemp(prefix=f"sf_{key}_")
        self.ctx = br.new_context(viewport={"width": viewport[0], "height": viewport[1]}, device_scale_factor=2,
                                  locale="vi-VN" if LANG == "vi" else "en-US", storage_state=storage,
                                  record_video_dir=self.dir, record_video_size={"width": viewport[0], "height": viewport[1]})
        self.ctx.add_init_script(INIT_JS)
        self.pg = self.ctx.new_page(); self.t_open = time.monotonic(); self.t0 = self.t1 = None

    def start(self):
        self.pg.mouse.move(self.vp[0] - 3, self.vp[1] - 3)
        self.pg.wait_for_timeout(300); self.t0 = time.monotonic() - self.t_open; self.pg.wait_for_timeout(700)

    def stop(self, hold=1500):
        self.pg.wait_for_timeout(hold); self.t1 = time.monotonic() - self.t_open

    def close(self):
        vpath = self.pg.video.path() if self.pg.video else None
        self.ctx.close()
        if self.t0 is not None and self.t1 is not None and vpath and os.path.exists(vpath):
            out = OUT / f"{self.key}.mp4"
            ss, dur = max(0.0, self.t0), self.t1 - self.t0
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ss:.2f}", "-i", vpath, "-t", f"{dur:.2f}",
                            "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-movflags", "+faststart", "-an", str(out)], check=True)
            d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                                     capture_output=True, text=True).stdout.strip() or 0)
            videos[self.key] = (out.name, self.vp[0], self.vp[1], round(d, 2))
            print(f"   video {out.name} {d:.1f}s")
        shutil.rmtree(self.dir, ignore_errors=True)


def tap(pg, sel, wait=1000, nth=0):
    loc = pg.locator(sel).nth(nth)
    loc.scroll_into_view_if_needed(); loc.click(); pg.wait_for_timeout(wait)


def digits(pg, s):
    for ch in s:
        pg.click(f".modal-content [data-numpad-key='{ch}']"); pg.wait_for_timeout(250)
    pg.wait_for_timeout(700)


def shop_floor(pg, wc=None, wo=None):
    """Open the Shop Floor, focus work center `wc` and wait until the card of work order `wo` is on the board."""
    for attempt in range(3):
        pg.goto(B + "/odoo/shop-floor")
        pg.wait_for_selector("[data-jobboard-cards], [data-workcenter-card]", timeout=30000); pg.wait_for_timeout(1500)
        if not wc:
            return
        try:
            pg.wait_for_selector(f"[data-workcenter-item='{wc}']", timeout=10000)
            pg.click(f"[data-workcenter-item='{wc}']"); pg.wait_for_timeout(2000)
            if wo: pg.wait_for_selector(f"[data-wo-card='{wo}']", timeout=10000)
            return
        except Exception:
            if attempt == 2: raise
            print("   retry board load")


def open_execute(pg, wc, wo):
    shop_floor(pg, wc, wo)
    pg.locator(f"[data-wo-card='{wo}'] [data-wo-product]").click()
    pg.wait_for_selector("[data-shopfloor-screen='execute']"); pg.wait_for_timeout(2000)


MODAL = "document.querySelector('.modal-content')"
Q = lambda sel: f"document.querySelector({json.dumps(sel)})"
QA = lambda sel: f"[...document.querySelectorAll({json.dumps(sel)})]"


def snap(pg, key, desc, boxes=()):
    pg.wait_for_timeout(400)
    SH.snap(pg, f"{key}.png", desc, boxes)


def scene(name):
    def deco(f):
        def run(*a):
            print("scene", name)
            try: f(*a)
            except Exception as e:   # one scene failing must not leave the others or the cleanup undone
                failed.append(name); print("  !! scene failed:", name, log_err(e))
        return run
    return deco


# ---------------------------------------------------------------- scenes
def run_scenes(br, storage, A, B_):
    moA, woA, rawA = A
    moB, woB = B_
    w1 = woA[0]; wqc = woB[3]
    inox, bolt = rawA

    def new(key, vp=PORTRAIT):
        return Scene(br, storage, key, vp)

    @scene("choose")
    def s_choose():
        rpc("viin.mrp.shopfloor.session", "action_set_workcenters", [])
        s = new("choose"); pg = s.pg
        try:
            shop_floor(pg); pg.wait_for_selector("[data-workcenter-card]"); s.start()
            tap(pg, f"[data-workcenter-card='{WC_LASER}']"); tap(pg, f"[data-workcenter-card='{WC_MILL}']")
            snap(pg, "choose", "Work-center selection: laser cutting and CNC milling selected, counter 2 selected",
                 [("cards", QA(f"[data-workcenter-card='{WC_LASER}'], [data-workcenter-card='{WC_MILL}']")), ("counter", Q("[data-selected-count]"))])
            tap(pg, "[data-confirm-workcenters]", 2500); s.stop()
        finally: s.close()

    @scene("jobboard")
    def s_jobboard():
        s = new("jobboard", LANDSCAPE); pg = s.pg
        try:
            shop_floor(pg, WC_MILL); s.start()
            for t in ("ready", "running", "waiting", "all"):
                tap(pg, f"[data-filter-tab='{t}']", 1200)
            snap(pg, "jobboard", "Job board of CNC milling on a landscape tablet, status tabs and job cards",
                 [("tabs", QA("[data-filter-tab]"))]); s.stop(1000)
        finally: s.close()

    @scene("behalf")
    def s_behalf():
        s = new("behalf"); pg = s.pg
        try:
            shop_floor(pg, WC_LASER, w1); s.start()
            tap(pg, f"[data-wo-card='{w1}'] [data-wo-product]", 2000)
            tap(pg, "[data-action-button='on-behalf']", 1500)
            tap(pg, "[data-employee-scope-tab='whole_plant']", 1000)
            tap(pg, f"[data-employee-option][data-employee-id='{EMP_OTHER}']", 1500)
            pg.locator("[data-cost-consequence]").scroll_into_view_if_needed(); pg.wait_for_timeout(900)
            s.stop()
            snap(pg, "behalf", "On behalf: shift credited to Le Minh Duc, card on the labour cost consequence",
                 [("cost", Q("[data-cost-consequence]")), ("employee", Q(f"[data-employee-id='{EMP_OTHER}']"))])
            tap(pg, "[data-reset-to-self]", 1200)
        finally: s.close()
        # work credited to the other employee (same server calls as the tablet with that choice): time line + output 1
        ctx = {"shopfloor_credited_employee_id": EMP_OTHER}
        rpc("mrp.workorder", "action_shopfloor_start", [w1], ctx=ctx); time.sleep(8)
        rpc("mrp.workorder", "action_shopfloor_record_production", [w1], 1, ctx=ctx)
        rpc("mrp.workorder", "action_shopfloor_pause", [w1], ctx=ctx)

    @scene("start")
    def s_start():
        s = new("start"); pg = s.pg
        try:
            shop_floor(pg, WC_LASER, w1); s.start()
            tap(pg, f"[data-wo-card='{w1}'] [data-wo-action-button]", 3500)
            pg.wait_for_selector("[data-shopfloor-screen='execute'] [data-action-button='pause']")
            s.stop(1000)
            snap(pg, "start", "Operation screen: laser cutting running with live timer, Pause / Stop machine / Finish",
                 [("timer", Q("[data-execute-timer]")), ("actions", Q("[data-shopfloor-screen='execute'] [data-action-row]"))])
        finally: s.close()

    @scene("output")
    def s_output():
        s = new("output"); pg = s.pg
        try:
            open_execute(pg, WC_LASER, w1); s.start()
            tap(pg, "[data-action-button='record-production']", 1500)
            digits(pg, "3")
            snap(pg, "output", "Record output: 3 typed on the number pad before confirming",
                 [("numpad", Q("[data-quantity-pad]") + "||" + Q(".modal-content [data-numpad-section='grid']"))])
            tap(pg, "[data-action-button='confirm-quantity']", 2500); s.stop()
            snap(pg, "undo", "After confirming: Recorded 4 / 8 with the Undo last recording area",
                 [("undo", Q("[data-undo-action]")), ("recorded", Q("[data-quantity-context]"))])
        finally: s.close()

    @scene("undo")
    def s_undo():
        s = new("undo_video"); s.key = "undo"; pg = s.pg
        try:
            open_execute(pg, WC_LASER, w1)
            tap(pg, "[data-action-button='record-production']", 1500); s.start()
            pg.locator("[data-undo-action] button").first.click(); pg.wait_for_timeout(2500); s.stop()
        finally: s.close()
        rpc("mrp.workorder", "action_shopfloor_record_production", [w1], 3)   # back to 4 / 8 for the next scenes

    @scene("materials")
    def s_materials():
        rpc("mrp.workorder", "action_shopfloor_record_consumption", [w1], bolt, 96)   # bolts as expected -> Enough
        s = new("materials"); pg = s.pg
        try:
            open_execute(pg, WC_LASER, w1); s.start()
            tap(pg, "[data-action-button='materials']", 1500)
            tap(pg, "[data-add-component]", 1100)
            pg.locator("[data-component-query]").click(); pg.keyboard.type("NVL-SON", delay=120); pg.wait_for_timeout(1200)
            tap(pg, "[data-component-option='376']", 1100)
            digits(pg, "2")
            tap(pg, ".modal-content [data-action-button='confirm']", 1800)
            pg.wait_for_selector("[data-materials-list]")
            s.stop()
            snap(pg, "materials", "Materials: expected vs actual, Short / Enough chips, powder coat added outside the BOM",
                 [("badges", QA("[data-material-chip], [data-material-extra]"))])
        finally: s.close()

    @scene("scrap")
    def s_scrap():
        s = new("scrap"); pg = s.pg
        try:
            open_execute(pg, WC_LASER, w1); s.start()
            tap(pg, "[data-action-button='scrap']", 1500)
            tap(pg, "[data-scrap-products] [data-choice-item='374']", 1500)
            digits(pg, "2"); s.stop()
            snap(pg, "scrap", "Scrap: stainless sheet, irreversible warning and number pad (not confirmed)",
                 [("warning", Q("[data-irreversible-warning]")), ("numpad", Q(".modal-content [data-numpad-section='grid']"))])
            pg.click(".modal-content [data-action-button='cancel']"); pg.wait_for_timeout(1500)   # never confirm scrap
        finally: s.close()

    @scene("maint")
    def s_maint():
        s = new("maint"); pg = s.pg
        try:
            open_execute(pg, WC_LASER, w1); s.start()
            tap(pg, "[data-action-button='incident']", 1500)
            pg.locator("[data-viin-maintenance-action='report-breakdown']").scroll_into_view_if_needed(); pg.wait_for_timeout(600)
            s.stop()
            snap(pg, "maint", "Stop machine screen with the Equipment failure - call maintenance option (not tapped)",
                 [("maint", Q("[data-viin-maintenance-action='report-breakdown']") + ".closest('.o_viin_sf_maintenance_panel')")])
        finally: s.close()

    @scene("stop")
    def s_stop():
        s = new("stop"); pg = s.pg
        try:
            open_execute(pg, WC_LASER, w1); s.start()
            tap(pg, "[data-action-button='incident']", 1500)
            snap(pg, "stop", "Stop machine: reason tiles, one tap stops the station", [("tiles", Q("[data-incident-reasons]"))])
            tap(pg, f"[data-incident-reasons] [data-choice-item='{LOSS_SETUP}']", 2500); s.stop()
        finally: s.close()

    @scene("restart")
    def s_restart():
        s = new("restart"); pg = s.pg
        try:
            shop_floor(pg, WC_LASER, w1); s.start()
            tap(pg, f"[data-wo-card='{w1}'] [data-wo-action-button]", 2500)
            pg.wait_for_selector("[data-restart-station]")
            snap(pg, "restart", "Manager opens the stopped station: reason and the Restart station button",
                 [("restart", Q("[data-execute-stopped]") + "||" + Q("[data-restart-station]"))])
            tap(pg, "[data-restart-station]", 1200); tap(pg, "[data-restart-confirm]", 2500); s.stop()
        finally: s.close()

    @scene("close")
    def s_close():
        rpc("viin.mrp.shopfloor.session", "action_set_workcenters", [WC_LASER, WC_MILL, WC_QC])   # choose saved only 2 stations
        s = new("close"); pg = s.pg
        try:
            open_execute(pg, WC_QC, wqc); s.start()
            tap(pg, "[data-action-button='finish']", 3000)
            pg.wait_for_selector("[data-confirm-order]")
            if pg.locator("[data-quality-action='pass']").count():
                tap(pg, "[data-quality-action='pass']", 2000)
            tap(pg, "[data-confirm-order]", 3500)
            pg.wait_for_selector("[data-backorder-decision]"); pg.locator("[data-backorder-decision]").scroll_into_view_if_needed()
            pg.wait_for_timeout(800); s.stop()
            snap(pg, "close", "Close order screen: 5 of 8 produced, backorder question (answered Back, order stays open)",
                 [("backorder", Q("[data-backorder-decision]"))])
            pg.click("[data-cancel-confirm]"); pg.wait_for_timeout(2000)   # never close the order
        finally: s.close()

    @scene("approval")
    def s_approval():
        rpc("mrp.production", "write", [moB], {"consumption": "strict"})
        rpc("mrp.workorder", "action_shopfloor_record_consumption", [wqc], st["inoxB"], 52)
        s = new("approval"); pg = s.pg
        try:
            shop_floor(pg, WC_QC, wqc); s.start()
            tap(pg, f"[data-wo-card='{wqc}'] [data-wo-action-button]", 2500)
            tap(pg, "[data-confirm-order]", 3500)
            pg.wait_for_selector("[data-consumption-differences]"); pg.locator("[data-consumption-differences]").scroll_into_view_if_needed()
            pg.wait_for_timeout(800); s.stop()
            snap(pg, "approval", "Close screen with the table materials used differ from the BOM (strict consumption on the copy)",
                 [("diff", Q("[data-consumption-differences]"))])
            pg.click("[data-cancel-confirm]"); pg.wait_for_timeout(2000)
        finally: s.close()

    @scene("labour")
    def s_labour():
        s = new("labour", LANDSCAPE); pg = s.pg
        try:
            pg.goto(B + f"/odoo/action-mrp.mrp_workorder_todo/{w1}"); pg.wait_for_selector(".o_form_view .o_notebook"); pg.wait_for_timeout(2000)
            pg.locator(".o_notebook .nav-link").nth(1).click(); pg.wait_for_timeout(1000); s.start()
            pg.locator(".o_notebook .nav-link").nth(0).click(); pg.wait_for_timeout(1500); s.stop()
            snap(pg, "labour", "Work order form, Time Tracking: lines credited to Le Minh Duc (on behalf) and Pham Thu Trang",
                 [("employee", Q(".o_field_widget[name=time_ids] table"))])
        finally: s.close()

    @scene("entries")
    def s_entries():
        s = new("entries", LANDSCAPE); pg = s.pg
        try:
            pg.goto(B + "/odoo/action-viin_mrp_workorder.viin_mrp_shopfloor_entry_action"); pg.wait_for_selector(".o_list_view"); pg.wait_for_timeout(2000)
            s.start()
            tap(pg, ".o_searchview_dropdown_toggler", 1200)
            snap(pg, "entries", "Shop Floor Entries with the Filters / Group By panel open", [("filters", Q(".o_search_bar_menu") + "||" + Q(".o-dropdown--menu"))])
            menu = lambda t: pg.locator(".o_search_bar_menu .o_menu_item, .o-dropdown--menu .o_menu_item", has_text=t).first
            menu(T["undone"]).click(); pg.wait_for_timeout(1800)
            menu(T["undone"]).click(); pg.wait_for_timeout(600)
            menu(T["behalf"]).click(); pg.wait_for_timeout(1800); s.stop()
        finally: s.close()

    @scene("desktop")
    def s_desktop():
        s = new("desktop", LANDSCAPE); pg = s.pg
        card = (f"[...document.querySelectorAll('.o_kanban_record')].find(c=>[...c.querySelectorAll('*')]"
                f".some(e=>e.children.length==0&&e.textContent.trim()==={json.dumps(T['laser'])}))")
        try:
            pg.goto(B + "/odoo/action-mrp.mrp_workcenter_kanban_action"); pg.wait_for_selector(".o_kanban_record"); pg.wait_for_timeout(2500)
            s.start()
            snap(pg, "desktop", "Manufacturing > Overview: laser cutting card with the open shop floor screen button",
                 [("card", card), ("button", card + ".querySelector('button[name=action_open_shop_floor_from_workcenter]')")])
            btn = pg.evaluate_handle(card + ".querySelector('button[name=action_open_shop_floor_from_workcenter]')").as_element()
            btn.click(); pg.wait_for_selector("[data-jobboard-cards]"); pg.wait_for_timeout(2500); s.stop()
        finally: s.close()

    for f in (s_choose, s_jobboard, s_behalf, s_start, s_output, s_undo, s_materials, s_scrap, s_maint, s_stop, s_restart,
              s_close, s_approval, s_labour, s_entries, s_desktop):
        f()


# ---------------------------------------------------------------- main
def main():
    global st
    if STATE.exists():
        print("cleaning what the previous run left:"); st = json.loads(STATE.read_text())
        print(" left:", cleanup()); restore_env()
    st = {"mos": [], "moves": [], "prod_baseline": None, "lang_changed": False, "en_applied": False}; save_state()
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*"):
        f.unlink()
    left = {}
    try:
        if LANG == "en":
            st["en_applied"] = True; save_state(); en_names()
            rpc("res.users", "write", [2], {"lang": "en_US"}); st["lang_changed"] = True; save_state()
        last = rpc("mrp.workcenter.productivity", "search", [], order="id desc", limit=1)
        st["prod_baseline"] = last[0] if last else 0; save_state()
        src = rpc("mrp.production", "search", [("name", "=", SRC_MO), ("company_id", "=", NM)])[0]
        # copy A: operator scenes on the laser station; its components are recorded on that first operation
        moA, nameA, woA, rawA = copy_mo(src)
        rpc("stock.move", "write", rawA, {"workorder_id": woA[0]})
        raw_by_prod = {m["product_id"][0]: m["id"] for m in rpc("stock.move", "read", rawA, ["product_id"])}
        A = (moA, woA, [raw_by_prod[374], raw_by_prod[375]])
        # copy B: laser, bending, welding finished; 5 of 8 recorded on the QC operation, which is running
        moB, nameB, woB, rawB = copy_mo(src)
        for w in woB[:3]:
            rpc("mrp.workorder", "action_shopfloor_start", [w]); rpc("mrp.workorder", "action_shopfloor_finish_operation", [w])
        rpc("mrp.workorder", "action_shopfloor_record_production", [woB[3]], 5)
        rpc("mrp.workorder", "action_shopfloor_start", [woB[3]])
        st["inoxB"] = {m["product_id"][0]: m["id"] for m in rpc("stock.move", "read", rawB, ["product_id"])}[374]; save_state()
        print("copies:", nameA, woA, "/", nameB, woB)
        rpc("viin.mrp.shopfloor.session", "action_set_workcenters", [WC_LASER, WC_MILL, WC_QC])
        with sync_playwright() as p:
            br = p.chromium.launch(channel="chrome")
            try:
                lp = new_page(br, viewport=PORTRAIT)
                storage = str(Path(tempfile.gettempdir()) / f"sf_storage_{LANG}.json"); lp.context.storage_state(path=storage); lp.context.close()
                run_scenes(br, storage, A, (moB, woB))
            finally:
                br.close()
    finally:
        print("cleanup:")
        left = cleanup()
        try: rpc("viin.mrp.shopfloor.session", "action_set_workcenters", [])   # admin had no saved stations before
        except RuntimeError as e: print("COULD NOT reset shop floor session", log_err(e))
        restore_env()
        if not left: STATE.unlink(missing_ok=True)
        print("LEFT BEHIND:", left or "nothing")
    for s_ in SH.shots:
        k = s_["file"].rsplit(".", 1)[0]
        if k in videos:
            f, w, h, d = videos[k]; s_.update(video=f, video_w=w, video_h=h, duration=d)
    SH.save()
    print("failed scenes:", failed or "none")
    print("produced:", [(s_["file"], s_["w"], s_["h"], [b["label"] for b in s_["boxes"]], s_.get("duration")) for s_ in SH.shots])


if __name__ == "__main__":
    main()
