#!/usr/bin/env python3
"""
svg_to_vector.py
Batch-converts SVG files to Android VectorDrawable XML.

Output: vectordrawable/ (flat directory) at workspace root.
Files with CJK / Korean / '=' characters in filename are skipped.
"""

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"


def _resolve_workspace() -> Path:
    parser = argparse.ArgumentParser(
        description="Batch-convert SVG files to Android VectorDrawable XML."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Root folder containing SVG files (default: folder containing this script)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output folder (default: <root>/vectordrawable)",
    )
    args, _ = parser.parse_known_args()
    root = (args.root or Path(__file__).parent).resolve()
    out  = (args.out  or root / "vectordrawable").resolve()
    return root, out


WORKSPACE, OUTPUT_DIR = _resolve_workspace()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def has_special_chars(name: str) -> bool:
    """Return True if filename contains non-ASCII chars or '='."""
    for ch in name:
        if ord(ch) > 127 or ch == '=':
            return True
    return False


def sanitize_name(name: str) -> str:
    """Convert an SVG basename to a valid Android drawable resource name."""
    name = name.lower()
    name = re.sub(r'[\s\-]+', '_', name)       # spaces / dashes → underscore
    name = re.sub(r'[^a-z0-9_]', '', name)     # drop everything else
    name = re.sub(r'_+', '_', name)            # collapse repeated underscores
    name = name.strip('_')
    if not name:
        name = "icon"
    if name[0].isdigit():
        name = "ic_" + name
    return name


def parse_transform_translate(transform_str):
    """Extract (tx, ty) from 'translate(x, y)' or 'translate(x y)'."""
    if not transform_str:
        return 0.0, 0.0
    m = re.search(r'translate\(\s*([\d.\-]+)[\s,]+([\d.\-]+)\s*\)', transform_str)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r'translate\(\s*([\d.\-]+)\s*\)', transform_str)
    if m:
        return float(m.group(1)), 0.0
    return 0.0, 0.0


def rect_to_path(x, y, w, h) -> str:
    x, y, w, h = float(x), float(y), float(w), float(h)
    return f"M{x},{y} L{x+w},{y} L{x+w},{y+h} L{x},{y+h} Z"


def circle_to_path(cx, cy, r) -> str:
    cx, cy, r = float(cx), float(cy), float(r)
    # Two 180° arcs that together form a full circle
    return (
        f"M{cx - r},{cy} "
        f"A{r},{r},0,1,0,{cx + r},{cy} "
        f"A{r},{r},0,1,0,{cx - r},{cy} Z"
    )


def ns_tag(tag):
    return f"{{{SVG_NS}}}{tag}"


def parse_style(style_str) -> dict:
    result = {}
    if not style_str:
        return result
    for part in style_str.split(';'):
        part = part.strip()
        if ':' in part:
            k, v = part.split(':', 1)
            result[k.strip()] = v.strip()
    return result


def color_str(color):
    """Return a canonical hex color string, or None for 'none'/empty."""
    if not color:
        return None
    color = color.strip()
    if color.lower() in ('none', ''):
        return None
    if color.startswith('#'):
        return color.upper()
    named = {
        'white':       '#FFFFFF',
        'black':       '#000000',
        'red':         '#FF0000',
        'green':       '#008000',
        'blue':        '#0000FF',
        'transparent': None,
    }
    return named.get(color.lower(), color)


# ---------------------------------------------------------------------------
# Pre-collect <clipPath> definitions from <defs>
# ---------------------------------------------------------------------------

def collect_clip_paths(root_elem) -> dict:
    """Return a dict of {clip_id: path_data_string} from all <defs> in the SVG."""
    clips = {}
    for defs in root_elem.iter(ns_tag('defs')):
        for clip in defs.iter(ns_tag('clipPath')):
            clip_id = clip.get('id', '')
            if not clip_id:
                continue
            path_parts = []
            for child in clip:
                ctag = child.tag
                if ctag == ns_tag('rect'):
                    x  = child.get('x', '0')
                    y  = child.get('y', '0')
                    w  = child.get('width',  '0')
                    h  = child.get('height', '0')
                    tx, ty = parse_transform_translate(child.get('transform', ''))
                    path_parts.append(
                        rect_to_path(float(x) + tx, float(y) + ty, float(w), float(h))
                    )
                elif ctag == ns_tag('path'):
                    d = child.get('d', '')
                    if d:
                        path_parts.append(d)
                elif ctag == ns_tag('circle'):
                    path_parts.append(circle_to_path(
                        child.get('cx', '0'),
                        child.get('cy', '0'),
                        child.get('r',  '0'),
                    ))
            clips[clip_id] = ' '.join(path_parts)
    return clips


# ---------------------------------------------------------------------------
# Element conversion
# ---------------------------------------------------------------------------

def process_element(elem, clips, depth=1, inherited=None):
    """
    Recursively convert an SVG element (and its children) to a list of
    VectorDrawable XML lines.
    """
    if inherited is None:
        inherited = {}

    lines      = []
    indent     = '    ' * depth
    sub_indent = indent + '    '
    tag        = elem.tag

    # Merge inline style + element attributes for downstream inheritance
    style        = parse_style(elem.get('style', ''))
    current_attrs = dict(inherited)
    for attr_name in ('fill', 'fill-opacity', 'fill-rule',
                      'stroke', 'stroke-width', 'stroke-opacity'):
        v = style.get(attr_name) or elem.get(attr_name)
        if v:
            current_attrs[attr_name] = v

    # --- <defs>: already processed; skip entirely ---
    if tag == ns_tag('defs'):
        return []

    # --- Drawable shapes: <path>, <circle>, <rect> ---
    if tag in (ns_tag('path'), ns_tag('circle'), ns_tag('rect')):
        if tag == ns_tag('path'):
            path_data = elem.get('d', '')
        elif tag == ns_tag('circle'):
            path_data = circle_to_path(
                elem.get('cx', '0'),
                elem.get('cy', '0'),
                elem.get('r',  '0'),
            )
        else:  # rect
            path_data = rect_to_path(
                elem.get('x', '0'),
                elem.get('y', '0'),
                elem.get('width',  '0'),
                elem.get('height', '0'),
            )

        if not path_data:
            return []

        # Resolve fill / stroke with style > element > inherited > defaults
        def resolve(key, default=''):
            return style.get(key) or elem.get(key) or current_attrs.get(key, default)

        fill       = resolve('fill', '#000000')
        fill_opac  = resolve('fill-opacity')
        fill_rule  = resolve('fill-rule')
        stroke     = resolve('stroke')
        sw         = resolve('stroke-width')
        so         = resolve('stroke-opacity')

        fill_color   = color_str(fill)
        stroke_color = color_str(stroke)

        attrs = []
        if fill_color:
            attrs.append(f'android:fillColor="{fill_color}"')
        if fill_opac:
            attrs.append(f'android:fillAlpha="{fill_opac}"')
        if fill_rule and fill_rule.lower() == 'evenodd':
            attrs.append('android:fillType="evenOdd"')
        if stroke_color:
            attrs.append(f'android:strokeColor="{stroke_color}"')
        if sw:
            attrs.append(f'android:strokeWidth="{sw}"')
        if so:
            attrs.append(f'android:strokeAlpha="{so}"')
        attrs.append(f'android:pathData="{path_data}"')

        if len(attrs) == 1:
            lines.append(f'{indent}<path {attrs[0]}/>')
        else:
            attrs_xml = f'\n{sub_indent}'.join(attrs)
            lines.append(f'{indent}<path\n{sub_indent}{attrs_xml}/>')
        return lines

    # --- <g>: may carry a clip-path reference ---
    if tag == ns_tag('g'):
        clip_attr = elem.get('clip-path', '')
        m = re.match(r'url\(#(.+?)\)\s*$', clip_attr.strip())
        if m:
            clip_id        = m.group(1)
            clip_path_data = clips.get(clip_id, '')
            lines.append(f'{indent}<group>')
            if clip_path_data:
                lines.append(
                    f'{sub_indent}<clip-path android:pathData="{clip_path_data}"/>'
                )
            for child in elem:
                lines.extend(process_element(child, clips, depth + 1, current_attrs))
            lines.append(f'{indent}</group>')
        else:
            # Plain group — flatten (process children at same depth)
            for child in elem:
                lines.extend(process_element(child, clips, depth, current_attrs))
        return lines

    # --- Any other element: recurse into children ---
    for child in elem:
        lines.extend(process_element(child, clips, depth, current_attrs))
    return lines


# ---------------------------------------------------------------------------
# Main SVG → VectorDrawable conversion
# ---------------------------------------------------------------------------

def convert_svg(svg_path) -> str:
    tree = ET.parse(str(svg_path))
    root = tree.getroot()

    if root.tag != ns_tag('svg'):
        raise ValueError(f"Root element is not <svg>: {root.tag}")

    width   = root.get('width',  '24')
    height  = root.get('height', '24')
    viewbox = root.get('viewBox', '')

    if viewbox:
        parts = viewbox.strip().split()
        if len(parts) == 4:
            vp_w, vp_h = parts[2], parts[3]
        else:
            vp_w, vp_h = width, height
    else:
        vp_w, vp_h = width, height

    # Strip any unit suffix (px, pt, …) from width/height for android:width/height
    w_num = re.sub(r'[^\d.]', '', width)  or vp_w
    h_num = re.sub(r'[^\d.]', '', height) or vp_h

    clips = collect_clip_paths(root)

    body_lines = []
    for child in root:
        body_lines.extend(process_element(child, clips, depth=1))

    body = '\n'.join(body_lines)
    sep  = '\n' if body else ''

    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
        f'    android:width="{w_num}dp"\n'
        f'    android:height="{h_num}dp"\n'
        f'    android:viewportWidth="{vp_w}"\n'
        f'    android:viewportHeight="{vp_h}">'
        f'{sep}{body}{sep}'
        '</vector>\n'
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    svg_files = sorted(WORKSPACE.rglob('*.svg'))
    # Exclude any SVGs that end up inside the output directory itself
    svg_files = [p for p in svg_files if OUTPUT_DIR not in p.parents]

    converted   = 0
    skipped     = 0
    errors      = 0
    name_counts = {}   # track used output names to handle collisions

    for svg_path in svg_files:
        basename = svg_path.stem  # filename without .svg

        if has_special_chars(basename):
            print(f"  SKIP  {svg_path.relative_to(WORKSPACE)}")
            skipped += 1
            continue

        san_name = sanitize_name(basename)

        # Collision handling: first use keeps bare name; subsequent get _2, _3 …
        if san_name in name_counts:
            name_counts[san_name] += 1
            out_name = f"{san_name}_{name_counts[san_name]}"
        else:
            name_counts[san_name] = 1
            out_name = san_name

        out_path = OUTPUT_DIR / f"{out_name}.xml"

        try:
            xml_content = convert_svg(svg_path)
            out_path.write_text(xml_content, encoding='utf-8')
            converted += 1
        except Exception as exc:
            print(f"  ERROR {svg_path.relative_to(WORKSPACE)}: {exc}")
            errors += 1

    print(f"\n{'=' * 55}")
    print(f"Converted : {converted}")
    print(f"Skipped   : {skipped}")
    print(f"Errors    : {errors}")
    print(f"Output    : {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
