#!/usr/bin/env python3
"""strings_audit.py - audit Android translations against the default strings.xml (standard library only).

Usage: python strings_audit.py <res-dir> [--default values] [--json]
Checks every values-<locale>/*.xml (merged, like Android does) against <res-dir>/values/*.xml:
  E missing-key        key in default but not in the locale (reported as a count + first 10)
  E extra-key          key in the locale but not in default (orphan)
  E placeholder        format specifiers differ (%1$s, %d, %s ...) between default and translation
  E plural-quantity    <plurals> missing quantities the language needs (Arabic: zero one two few many other)
  E apostrophe         unescaped ' in a value (breaks aapt) unless the value is quoted
  W untranslated       value identical to the default for a non-trivial string (>= 12 chars, has letters)
  W rtl-latin-only     RTL locale (ar, fa, ur, he, ps, sd, ug, yi) value with Latin letters only and no placeholders
Keys marked translatable="false" are ignored. Exit 1 on any error.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RTL = {"ar", "fa", "ur", "he", "iw", "ps", "sd", "ug", "yi"}
PLURALS = {"ar": {"zero", "one", "two", "few", "many", "other"}, "he": {"one", "two", "other"}, "iw": {"one", "two", "other"},
           "ru": {"one", "few", "many", "other"}, "uk": {"one", "few", "many", "other"}, "pl": {"one", "few", "many", "other"}}
SPEC = re.compile(r"%(?:\d+\$)?[-#+ 0,(]*\d*(?:\.\d+)?[a-zA-Z%]")


def load_dir(d):
    """Merge every *.xml in a values dir (strings.xml, strings_ads.xml, ...): Android merges them too."""
    strings, plurals, raw = {}, {}, ""
    for f in sorted(d.glob("*.xml")):
        try:
            s, p, r = load(f)
        except ET.ParseError:
            raise
        strings.update(s)
        plurals.update(p)
        raw += r
    return strings, plurals, raw


def load(path):
    root = ET.parse(path).getroot()
    strings, plurals = {}, {}
    if root.tag != "resources":
        return strings, plurals, ""
    for el in root:
        if el.get("translatable") == "false":
            continue
        if el.tag == "string":
            strings[el.get("name")] = "".join(el.itertext())
        elif el.tag == "plurals":
            plurals[el.get("name")] = {i.get("quantity"): "".join(i.itertext()) for i in el}
    raw = path.read_text(encoding="utf-8", errors="replace")
    return strings, plurals, raw


def specs(v):
    return sorted(s for s in SPEC.findall(v) if s != "%%")


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    res = Path(args[0])
    base = res / "values" / "strings.xml"
    if not base.exists():
        print(f"no default strings at {base}")
        return 2
    d_str, d_plu, _ = load_dir(res / "values")
    findings = []
    for loc_dir in sorted(res.glob("values-*")):
        if not any(loc_dir.glob("*.xml")):
            continue
        code = loc_dir.name[len("values-"):]
        lang = re.split(r"[-_]", code.replace("b+", ""))[0]
        if not re.fullmatch(r"[a-z]{2,3}(-r[A-Z]{2})?|b\+.+", code):
            continue
        try:
            strs, plu, raw = load_dir(loc_dir)
        except ET.ParseError as e:
            findings.append(("E", "xml-parse", code, "", str(e)))
            continue
        missing = sorted(set(d_str) - set(strs))
        if missing:
            findings.append(("E", "missing-key", code, "", f"{len(missing)} missing, first: {', '.join(missing[:10])}"))
        for k in sorted(set(strs) - set(d_str)):
            findings.append(("E", "extra-key", code, k, "not in default strings.xml"))
        for k, v in strs.items():
            if k not in d_str:
                continue
            if specs(v) != specs(d_str[k]):
                findings.append(("E", "placeholder", code, k, f"default {specs(d_str[k])} vs {specs(v)}"))
            if re.search(r"(?<!\\)'", v) and not (v.startswith('"') and v.endswith('"')):
                rawval = re.search(r'name="%s"[^>]*>(.*?)</string>' % re.escape(k), raw, re.S)
                if rawval and re.search(r"(?<!\\)'", rawval.group(1)) and not rawval.group(1).strip().startswith('"'):
                    findings.append(("E", "apostrophe", code, k, "unescaped apostrophe"))
            if v == d_str[k] and len(v) >= 12 and re.search(r"[A-Za-z]{3}", v) and lang != "en":
                findings.append(("W", "untranslated", code, k, "same as default"))
            if lang in RTL and not specs(v) and re.search(r"[A-Za-z]{4}", v) and not re.search(r"[\u0590-\u08FF]", v):
                findings.append(("W", "rtl-latin-only", code, k, "RTL locale value has only Latin letters"))
        need = PLURALS.get(lang)
        for k, q in plu.items():
            if need and not need.issubset(q):
                findings.append(("E", "plural-quantity", code, k, "missing " + ", ".join(sorted(need - set(q)))))
            if k in d_plu:
                for qn, qv in q.items():
                    base_specs = {tuple(specs(x)) for x in d_plu[k].values()}
                    if tuple(specs(qv)) not in base_specs:
                        findings.append(("E", "placeholder", code, f"{k}[{qn}]", "specifiers differ from default plural"))
    if "--json" in argv:
        print(json.dumps([dict(zip(("severity", "rule", "locale", "key", "message"), x)) for x in findings], indent=1))
    else:
        for sev, rule, code, key, msg in findings:
            print(f"{code} {sev} {rule} {key} {msg}".replace("  ", " "))
        e = sum(x[0] == "E" for x in findings)
        print(f"\n{len(findings)} findings ({e} errors, {len(findings) - e} warnings); default has {len(d_str)} strings")
    return 1 if any(x[0] == "E" for x in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
