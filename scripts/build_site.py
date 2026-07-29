#!/usr/bin/env python3
"""Convert a browser-saved Wayback Machine capture of nurse-riko.net into a
static site that can be served from https://nurse-rikox.web-rider.biz/000/.

Usage:
    python3 scripts/build_site.py SAVED.html [--assets DIR] [--out DIR]

The saved page references its assets two ways: as "./<name>_files/x" (the
browser's local copy) and as absolute web.archive.org URLs. Both are rewritten
to /000/assets/..., the Wayback toolbar and replay machinery are stripped, and
social widgets are pointed back at their live CDNs.
"""

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

BASE = "/000"
ASSETS = f"{BASE}/assets"
SAVED_DIR_RE = r"\./[^/\"']*_files/"

# Wayback replay wrappers: /web/<timestamp><flags>/<original-url>. The saved
# page uses both absolute and protocol-relative forms.
WAYBACK_RE = re.compile(
    r"(?:https?:)?//web\.archive\.org/web/\d{14}(?:im_|js_|cs_|if_|oe_|id_|_id)?/"
)
ORIGIN_RE = re.compile(r"https?://nurse-riko\.net")

# Saved-page artefacts that must not ship: Wayback replay code, archive
# analytics, access-counter beacons, and widget iframe internals that only ever
# existed inside the browser's save.
DROP_ASSETS = {
    "bundle-playback.js", "wombat.js", "ruffle.js", "athena.js",
    "banner-styles.css", "iconochive.css", "analytics.js",
    "ptb.js", "pta.js", "pts.js", "42718618.js", "social_count.php",
    "SocialCounts.js", "platform.js",
    "cb=gapi.loaded_0", "cb=gapi.loaded_1", "489248768542265344",
    "postmessageRelay.html", "fastbutton.html", "like.html", "button.html",
    "saved_resource.html", "saved_resource(1", "5oivrH7Newv.html",
    "5oivrH7Newv(1", "tweet_button.534c17036beb62f94dbf2b30b59dc118.ja.html",
    "button.e722c258c2de2a7c30637037cf3fc66c.js",
    "timeline.940f18f47befdb8f145753d04827500f.js",
}

# Third-party widgets restored to their live origins rather than served stale.
CDN = {
    "widgets.js": "https://platform.twitter.com/widgets.js",
    "sdk.js": "https://connect.facebook.net/ja_JP/sdk.js",
    "btn.js": "https://widgets.getpocket.com/v1/j/btn.js",
    "bookmark_button.js": "https://b.st-hatena.com/js/bookmark_button.js",
}

# Assets the site owns and must be present under assets/.
SITE_CSS = ["design.css", "mobile.css", "advanced.css", "print.css",
            "wpp.css", "style.css"]
SITE_JS = ["jquery.js", "jquery-migrate.min.js", "utility.js"]


def real_name(name: str) -> str:
    """Undo the browser's save-time mangling of a filename.

    Chrome appends ".ダウンロード" to scripts it cannot type-sniff and "(N)"
    to names that collide, so "foo(1).html" and "foo.html" are one asset.
    """
    name = re.sub(r"\.(ダウンロード|download)$", "", name)
    return re.sub(r"\((\d+)\)(?=\.|$)", "", name)


def strip_wayback_chrome(doc: str) -> str:
    """Remove the injected toolbar, replay bootstrap and browser-extension DOM."""
    doc = re.sub(
        r"<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->",
        "", doc, flags=re.S)
    doc = re.sub(r"<script[^>]*>\s*__wm\.init.*?</script>", "", doc, flags=re.S)
    doc = re.sub(r"<script[^>]*>[^<]*archive_analytics.*?</script>", "", doc, flags=re.S)
    doc = re.sub(r"<script[^>]*>\s*window\.RufflePlayer.*?</script>", "", doc, flags=re.S)
    doc = doc.replace("<!-- End Wayback Rewrite JS Include -->", "")
    # The toolbar reserved space via an inline custom property on <html>.
    doc = re.sub(r'(<html\b[^>]*?)\s*style="--wm-toolbar-height:[^"]*"', r"\1", doc)
    # Chrome/extension DOM appended after </body> is not part of the page.
    end = doc.rfind("</body>")
    if end != -1:
        doc = doc[:end] + "</body>\n</html>\n"
    return doc


def drop_tags_referencing(doc: str, names: set) -> str:
    """Delete <script>/<link> elements whose URL resolves to a dropped asset."""
    def keep(tag: str) -> bool:
        # A saved tag can carry several src attributes (the widget SDKs rewrite
        # them in place), so every URL in the tag has to clear the drop list.
        for url in re.findall(r'(?:src|href)="([^"]*)"', tag):
            leaf = real_name(html.unescape(url).split("?")[0].rstrip("/").split("/")[-1])
            if leaf in names or re.sub(r"\.\w+$", "", leaf) in names:
                return False
        return True

    doc = re.sub(r"<script\b[^>]*\bsrc=\"[^\"]*\"[^>]*>\s*</script>",
                 lambda m: m.group(0) if keep(m.group(0)) else "", doc)
    doc = re.sub(r"<link\b[^>]*>",
                 lambda m: m.group(0) if keep(m.group(0)) else "", doc)
    doc = re.sub(r"<iframe\b[^>]*>(?:.*?</iframe>)?",
                 lambda m: m.group(0) if keep(m.group(0)) else "", doc, flags=re.S)
    return doc


def rewrite_urls(doc: str) -> str:
    """Point every reference at /000/, resolving saved and archived forms alike."""
    # 1. Locally saved copies -> /000/assets/<real name>
    doc = re.sub(SAVED_DIR_RE + r"([^\"')\s>]+)",
                 lambda m: f"{ASSETS}/{real_name(html.unescape(m.group(1)))}", doc)

    # 2. Unwrap the Wayback replay prefix, leaving the original absolute URL.
    doc = WAYBACK_RE.sub("", doc)

    # 3. Original-origin URLs -> site-relative under /000.
    #    Theme/upload assets collapse into assets/ to match the saved folder,
    #    which is the only copy of them that exists.
    doc = re.sub(
        ORIGIN_RE.pattern + r"/wordpress/wp-content/[^\"')\s>]*?/([^/\"')\s>]+\.(?:png|jpe?g|gif|ico|css|js|svg))",
        lambda m: f"{ASSETS}/{m.group(1)}", doc)
    doc = ORIGIN_RE.sub(BASE, doc)

    # 4. Restore live CDNs for the social widgets worth keeping.
    for leaf, url in CDN.items():
        doc = doc.replace(f"{ASSETS}/{leaf}", url)

    # 5. Bare in-page anchors left behind by unwrapping (href="/000/#foo").
    doc = doc.replace(f'href="{BASE}/#', 'href="#')

    # 6. The save captured the Facebook widget mid-render, freezing the old
    #    canonical URL into its state attributes. Drop them so the SDK
    #    re-renders against whatever host actually serves the page.
    doc = re.sub(r'\s(?:fb-xfbml-state|fb-iframe-plugin-query)="[^"]*"', "", doc)
    doc = re.sub(r'<div class="fb-like fb_iframe_widget"',
                 '<div class="fb-like"', doc)
    return doc


def rewrite_css(text: str) -> tuple[str, set]:
    """Point a stylesheet's url() targets at assets/ and report the leaf names.

    Saved stylesheets keep Wayback's own rewriting ("/web/<ts>im_/http://...")
    alongside theme-relative paths, neither of which resolves once the CSS is
    served from /000/assets/.
    """
    wanted = set()

    def repl(m: re.Match) -> str:
        quote, url = m.group(1), m.group(2).strip()
        if url.startswith(("data:", "http://", "https://", "//", "#")):
            return m.group(0)
        leaf = html.unescape(url.split("?")[0].split("#")[0]).split("/")[-1]
        if not leaf:
            return m.group(0)
        wanted.add(leaf)
        return f"url({quote}{ASSETS}/{leaf}{quote})"

    text = re.sub(r"url\((['\"]?)([^)'\"]+)\1\)", repl, text)
    return text, wanted


def build(saved: Path, assets_src: Path | None, out: Path) -> None:
    doc = saved.read_text(encoding="utf-8", errors="replace")
    doc = strip_wayback_chrome(doc)
    doc = drop_tags_referencing(doc, DROP_ASSETS)
    doc = rewrite_urls(doc)
    doc = drop_tags_referencing(doc, DROP_ASSETS)  # catch post-rewrite leaves

    out_assets = out / "assets"
    out_assets.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(doc, encoding="utf-8")

    # The rewritten page is the authority on what ships. Anything it does not
    # reference is save-time debris -- the Wayback toolbar alone drags in a
    # jQuery UI bundle and a dozen collection thumbnails.
    referenced = sorted({
        m.group(1) for m in re.finditer(re.escape(ASSETS) + r"/([^\"')\s>]+)", doc)
    })
    (out / "ASSETS.txt").write_text("\n".join(referenced) + "\n", encoding="utf-8")
    wanted = set(referenced)

    # Stylesheets pull in a second tier of assets (backgrounds, icons) that the
    # page never names, so they have to be scanned before anything is pruned.
    css_wanted: set = set()
    if assets_src and assets_src.is_dir():
        for src in sorted(assets_src.iterdir()):
            if src.is_file() and real_name(src.name) in wanted and src.suffix == ".css":
                _, w = rewrite_css(src.read_text(encoding="utf-8", errors="replace"))
                css_wanted |= w
    wanted |= css_wanted

    kept = pruned = 0
    if assets_src and assets_src.is_dir():
        in_place = assets_src.resolve() == out_assets.resolve()
        for src in sorted(assets_src.iterdir()):
            if not src.is_file() or src.name == ".gitkeep":
                continue
            name = real_name(src.name)
            if name not in wanted:
                if in_place:
                    src.unlink()
                pruned += 1
                continue
            dest = out_assets / name
            if src != dest:
                shutil.copy2(src, dest)
                if in_place:
                    src.unlink()
            kept += 1

        # Rewrite the shipped copies now that they are in their final home.
        for css in sorted(out_assets.glob("*.css")):
            text, _ = rewrite_css(css.read_text(encoding="utf-8", errors="replace"))
            css.write_text(text, encoding="utf-8")

    present = {p.name for p in out_assets.iterdir() if p.is_file()}

    # A save never fetches <link rel=icon>/<meta og:image> targets, so the
    # full-size original can be absent while WordPress's resized derivative
    # survives. Same image -- repoint rather than ship a 404.
    substituted = []
    for name in [n for n in referenced if n not in present]:
        stem, dot, ext = name.rpartition(".")
        if not dot:
            continue
        variant = next((p for p in sorted(present)
                        if re.fullmatch(re.escape(stem) + r"-\d+x\d+\." + re.escape(ext), p)), None)
        if variant:
            doc = doc.replace(f"{ASSETS}/{name}", f"{ASSETS}/{variant}")
            substituted.append(f"{name} -> {variant}")
    if substituted:
        (out / "index.html").write_text(doc, encoding="utf-8")
        referenced = sorted({
            m.group(1) for m in re.finditer(re.escape(ASSETS) + r"/([^\"')\s>]+)", doc)
        })
        (out / "ASSETS.txt").write_text("\n".join(referenced) + "\n", encoding="utf-8")
        for s in substituted:
            print(f"  substituted {s}")

    missing = [n for n in referenced if n not in present]
    missing_css = sorted(n for n in css_wanted if n not in present)

    if missing or missing_css:
        (out / "MISSING.txt").write_text(
            "".join(f"{n}\n" for n in missing + missing_css), encoding="utf-8")

    print(f"wrote {out/'index.html'} ({len(doc):,} bytes)")
    print(f"page assets: {len(referenced)} referenced, kept {kept}, pruned {pruned}")
    print(f"css-referenced images: {len(css_wanted)}")
    for group, names in (("css", SITE_CSS), ("js", SITE_JS)):
        absent = [n for n in names if n not in present]
        if absent:
            print(f"  missing {group}: {', '.join(absent)}")
    if missing:
        print(f"MISSING from page: {', '.join(missing)}")
    if missing_css:
        print(f"MISSING theme images ({len(missing_css)}), first 5: "
              f"{', '.join(missing_css[:5])} ... see MISSING.txt")
    if not (missing or missing_css):
        print("all referenced assets present")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("saved", type=Path, help="the saved .html file")
    ap.add_argument("--assets", type=Path, default=None,
                    help='the companion "..._files" folder, if available')
    ap.add_argument("--out", type=Path, default=Path("site/000"))
    a = ap.parse_args()
    if not a.saved.is_file():
        print(f"no such file: {a.saved}", file=sys.stderr)
        return 1
    build(a.saved, a.assets, a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
