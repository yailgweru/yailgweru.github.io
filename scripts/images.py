"""Tinified, right-sized copies ("variants") of the site's images.

The site never serves a source image. Every <img> points at variants made
for the size it is shown at, so a 4 MB phone photo becomes a few KB of
avatar:

  team photos     assets/team/<slug>.*       -> assets/team/thumbs/      96, 192, 288, 480 px squares
  project images  assets/projects/<slug>.*   -> assets/projects/thumbs/  480, 960 px wide
  other local images in data.json            -> <their folder>/thumbs/   480, 960 px wide
  blog images     (drafts, via publish_blog.py) -> assets/blogs/<slug>/  480, 960, 1440 px wide

"Tinified" the way TinyPNG/TinyJPG do it: each image becomes a progressive
JPEG or a 256-colour PNG (libimagequant, the pngquant engine, with
dithering), whichever is smaller for it, so photos and smooth artwork end up
as JPEGs and diagrams, screenshots and flat graphics as crisp PNGs, whatever
format the source was saved in. Images with real transparency always stay
PNGs. EXIF data is dropped
after the orientation it records is applied, so phone photos don't publish
the GPS position they were taken at, and colours are converted to sRGB.

Variant names carry their size and a hash of the source and the recipe, e.g.
assets/team/thumbs/jane-doe.192x192.3f2a9c1b07.jpg. A variant is made once
and then reused; a changed photo gets new names, so no cache ever shows the
old one; and Pillow is only needed when something new has to be made.
"""
import glob
import hashlib
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RECIPE = "1"  # bump to remake every variant
JPEG_QUALITY = 80
# Portraits are cropped to a square around this point of their height (faces
# sit in the upper part of most portraits).
PORTRAIT_FOCUS = 0.3

PERSON_WIDTHS = (96, 192, 288, 480)  # 72-96px avatars at 1-3x; 480 for search engines
HERO_WIDTHS = (480, 960)
BLOG_WIDTHS = (480, 960, 1440)

NAME_RE = re.compile(r"^.+\.(\d+)x(\d+)\.[0-9a-f]{10}\.(jpg|png)$")
PASSTHROUGH = (".gif", ".svg")  # animated or vector: served as they are

_used = set()  # repo-relative paths of every variant handed out this run


def _rel(path):
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:  # e.g. a blog draft's image kept outside the repo
        return str(path)


def is_local_image(path):
    return bool(path) and not re.match(r"^https?://", str(path)) and Path(path).suffix.lower() not in PASSTHROUGH


def variants(src, widths, square=False, out_dir=None):
    """Variants of `src` (a path relative to the repo root, or absolute) at
    each width, made if missing. Returns [{"src", "w", "h"}], smallest first,
    with repo-relative paths. Sources are never upscaled, so a small source
    can yield fewer variants than widths asked for."""
    src_path = Path(src) if Path(src).is_absolute() else ROOT / src
    out_dir = Path(out_dir) if out_dir else src_path.parent / "thumbs"
    stem = src_path.stem
    base = f"{hashlib.sha1(src_path.read_bytes()).hexdigest()}|{RECIPE}|{int(square)}|{JPEG_QUALITY}"

    found, missing = {}, []
    for width in sorted(set(widths)):
        digest = hashlib.sha1(f"{base}|{width}".encode()).hexdigest()[:10]
        pattern = f"{glob.escape(str(out_dir))}/{glob.escape(stem)}.*x*.{digest}.*"
        matches = [Path(p) for p in glob.glob(pattern)]
        matches = [p for p in matches if NAME_RE.match(p.name)]
        if matches:
            found[width] = matches[0]
        else:
            missing.append((width, digest))
    if missing:
        found.update(_make(src_path, out_dir, stem, missing, square))

    out, seen = [], set()
    for width in sorted(found):
        path = found[width]
        w, h = (int(x) for x in NAME_RE.match(path.name).groups()[:2])
        rel = _rel(path)
        _used.add(rel)
        if w not in seen:  # a small source gives the same size for several widths
            seen.add(w)
            out.append({"src": rel, "w": w, "h": h})
    return out


def _make(src_path, out_dir, stem, wanted, square):
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit(f"Making thumbnails of {_rel(src_path)} needs Pillow: pip install pillow")
    im = _prepare(src_path, square)
    fmt = "png" if im.mode == "RGBA" else _best_format(im)
    out_dir.mkdir(parents=True, exist_ok=True)
    made = {}
    for width, digest in wanted:
        small = _resized(im, width, square)
        path = out_dir / f"{stem}.{small.width}x{small.height}.{digest}.{fmt}"
        path.write_bytes(_encode(small, fmt))
        print(f"  made {_rel(path)} ({max(1, path.stat().st_size // 1024)} KB)")
        made[width] = path
    return made


def _resized(im, width, square):
    from PIL import Image

    tw = min(width, im.width)
    th = tw if square else max(1, round(im.height * tw / im.width))
    return im.resize((tw, th), Image.LANCZOS, reducing_gap=3.0) if (tw, th) != im.size else im


def _encode(im, fmt):
    buf = io.BytesIO()
    if fmt == "png":
        _quantize(im).save(buf, "PNG", optimize=True)
    else:
        im.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    return buf.getvalue()


def _best_format(im):
    """"jpg" or "png", whichever is smaller for this image at 480px. Tried on
    real images, this picks JPEG for photos and smooth gradients (3-5x
    smaller) and PNG for diagrams and screenshots (crisper and smaller)."""
    test = _resized(im, 480, False)
    return "png" if len(_encode(test, "png")) < len(_encode(test, "jpg")) else "jpg"


def _prepare(src_path, square):
    """Open, apply EXIF orientation, convert to sRGB RGB/RGBA, square-crop."""
    from PIL import Image, ImageOps

    im = Image.open(src_path)
    im.load()
    im = ImageOps.exif_transpose(im)
    has_alpha = im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info)
    mode = "RGBA" if has_alpha else "RGB"
    icc = im.info.get("icc_profile")
    im = im.convert(mode)
    if icc:
        try:
            from PIL import ImageCms

            im = ImageCms.profileToProfile(
                im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), ImageCms.createProfile("sRGB"), outputMode=mode
            )
        except Exception:  # an odd profile shouldn't stop the build; colours may be a touch off
            pass
    if mode == "RGBA" and im.getchannel("A").getextrema()[0] == 255:
        im = im.convert("RGB")  # an alpha channel with no transparency in it: treat as a photo
    if square:
        w, h = im.size
        side = min(w, h)
        left = (w - side) // 2
        top = int((h - side) * PORTRAIT_FOCUS) if h > w else (h - side) // 2
        im = im.crop((left, top, left + side, top + side))
    return im


def _quantize(im):
    from PIL import Image, features

    method = Image.Quantize.LIBIMAGEQUANT if features.check("libimagequant") else Image.Quantize.FASTOCTREE
    return im.quantize(colors=256, method=method)


def srcset(items, prefix=""):
    return ", ".join(f"{prefix}{v['src']} {v['w']}w" for v in items)


def largest(items, at_most=None):
    """The largest variant, or the largest no wider than `at_most`."""
    fitting = [v for v in items if at_most is None or v["w"] <= at_most]
    return (fitting or items[:1])[-1]


def used_names(folder):
    """File names in `folder` of the variants handed out so far this run."""
    folder = Path(folder).resolve()
    return {Path(rel).name for rel in _used if (ROOT / rel).resolve().parent == folder}


def cleanup(folders):
    """Delete variants in these folders that nothing used this run (their
    source was replaced or removed). Returns the deleted paths."""
    removed = []
    for folder in folders:
        folder = ROOT / folder
        if not folder.is_dir():
            continue
        for path in sorted(folder.iterdir()):
            if NAME_RE.match(path.name) and _rel(path) not in _used:
                path.unlink()
                removed.append(_rel(path))
    return removed
