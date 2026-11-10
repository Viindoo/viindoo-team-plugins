"""Đổi ngôn ngữ giao diện của người dùng chụp màn trên hệ thống demo.

Chỉ đổi NHÃN Viindoo. Dữ liệu demo do mình bơm thì xem `dich_en.py` - hai việc khác nhau,
phải làm cả hai thì màn tiếng Anh mới sạch tiếng Việt.

Chạy:  python3 doi_ngon_ngu.py en     -> giao diện tiếng Anh
       python3 doi_ngon_ngu.py vi     -> trả lại tiếng Việt
       python3 doi_ngon_ngu.py        -> chỉ in ngôn ngữ hiện tại
"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("conn", os.path.join(HERE, "conn.py"))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
call = c.call

MA = {"en": "en_US", "vi": "vi_VN"}


def main():
    u = call("res.users", "read", [[c.UID], ["login", "lang"]])[0]
    if len(sys.argv) < 2:
        print("người dùng %s đang dùng %s" % (u["login"], u["lang"]))
        return
    ma = MA[sys.argv[1]]
    if not call("res.lang", "search", [[["code", "=", ma], ["active", "=", True]]]):
        sys.exit("ngôn ngữ %s chưa bật trên demo" % ma)
    call("res.users", "write", [[c.UID], {"lang": ma}])
    print("%s: %s -> %s" % (u["login"], u["lang"],
                            call("res.users", "read", [[c.UID], ["lang"]])[0]["lang"]))


if __name__ == "__main__":
    main()
