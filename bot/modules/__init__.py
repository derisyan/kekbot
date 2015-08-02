import os

module_blacklist = (
"__init__",
"util",
"chanapi",
)
temp = []

for fname in os.listdir(os.path.join(os.getcwd(), "bot/modules")):
	if "." in fname:
		base, ext = fname.rsplit(".", 1)
	else:
		base = fname
		ext = ""
	if (base not in module_blacklist) and (ext in ("", "py")):
		temp.append(base)

__all__ = temp