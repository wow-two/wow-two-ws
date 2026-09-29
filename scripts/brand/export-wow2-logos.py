#!/usr/bin/env python3
"""Export Panels with the recorded family seam-spacing refinement.

Requires Pillow and NumPy. No generated redraws, font substitution or upscaling.
Use --output-dir for a reproducibility check outside the saved brand directory.
"""

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / 'docs/brand/wow2'
SOURCE = BRAND / 'source/panels-approved.png'
SOURCE_SHA256 = '345550fdb7b72576649a3601651249fbbdb8f178bd8dafee6072fe69aec5347a'
REFERENCE = BRAND / 'source/wheelhouse-gap-reference.png'
REFERENCE_SHA256 = 'c3f5ef0b236a295bff2cd6a5aaf57736a993a0678a371cb86d862b373279916f'
NAVY = (35, 50, 79)
WHITE = (255, 255, 255)
PADDING = 8


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def components(mask, minimum=12):
    pending = mask.copy()
    groups = []
    height, width = pending.shape
    while pending.any():
        y, x = np.argwhere(pending)[0]
        queue = deque([(int(x), int(y))])
        pending[y, x] = False
        points = []
        while queue:
            x, y = queue.popleft()
            points.append((x, y))
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < width and 0 <= ny < height and pending[ny, nx]:
                    pending[ny, nx] = False
                    queue.append((nx, ny))
        if len(points) >= minimum:
            groups.append(points)
    return groups


def extract_alpha(image, box, expected_parts):
    """Unmatte the white page; preserve the selected contours and open counters."""
    rgb = np.asarray(image.crop(box).convert('RGB'), dtype=np.float32)
    groups = components(rgb.max(axis=2) < 160)
    if len(groups) != expected_parts:
        raise ValueError(f'Expected {expected_parts} source components; found {len(groups)}')
    solid = np.zeros(rgb.shape[:2], dtype=np.uint8)
    for group in groups:
        xs, ys = zip(*group)
        solid[ys, xs] = 255
    mask = Image.fromarray(solid)
    core = np.asarray(mask.filter(ImageFilter.MinFilter(3))) > 0
    band = np.asarray(mask.filter(ImageFilter.MaxFilter(3))) > 0
    ink = np.median(rgb[core], axis=0)
    page = np.array((254, 254, 254), dtype=np.float32)
    direction = page - ink
    alpha = np.clip(((page - rgb) * direction).sum(axis=2) / (direction * direction).sum(), 0, 1)
    alpha[~band] = 0
    alpha[alpha < 0.035] = 0
    alpha[core] = 1
    result = Image.fromarray(np.uint8(np.rint(alpha * 255)))
    bounds = result.getbbox()
    if not bounds:
        raise ValueError('Source crop is empty')
    return result.crop(bounds), {'crop': list(box), 'bounds_in_crop': list(bounds),
                                 'source_components': len(groups), 'source_ink_median': ink.tolist()}


def colorize(alpha, color):
    result = Image.new('RGBA', alpha.size, color + (0,))
    result.putalpha(alpha)
    return result


def harmonize_seams(alpha):
    """Widen facing edges; keep the source outside two tapered internal corridors."""
    # Centers fitted to the original opposing alpha=128 contours, in the tight source crop.
    lines = ((0.3423472537643413, 152.17292033255242, 20.197753896724457),
             (-0.35793912613671713, 513.6208336685615, 19.182332933972237))
    target = max(alpha.size) / 24
    source = np.asarray(alpha, dtype=float)
    result = source.copy()
    y, x = np.indices(source.shape)
    position = y / (alpha.height - 1)

    def smooth(value):
        value = np.clip(value, 0, 1)
        return value * value * (3 - 2 * value)

    profile = smooth((position - 0.37) / 0.14) * smooth((0.98 - position) / 0.14)
    for slope, intercept, original_gap in lines:
        width = original_gap + (target - original_gap) * profile
        normal_distance = np.abs(x - (slope * y + intercept)) / np.sqrt(1 + slope * slope)
        keep = np.clip(normal_distance - width / 2 + 0.5, 0, 1) * 255
        keep[profile == 0] = 255
        result = np.minimum(result, keep)
    output = Image.fromarray(np.uint8(np.rint(result)))
    if output.getbbox() != alpha.getbbox() or len(components(np.asarray(output) >= 128)) != 3:
        raise ValueError('Seam refinement changed the symbol bounds or panel count')
    return output, {'rule': 'visible maximum extent / 24', 'target_body_gap_px': target,
                    'target_gap_percent_height': target / alpha.height * 100,
                    'centerlines_x_equals_my_plus_b': [list(line) for line in lines],
                    'profile_y_fraction': {'ramp_in': [0.37, 0.51], 'body': [0.51, 0.84],
                                           'ramp_out': [0.84, 0.98]},
                    'method': 'alpha-only internal cuts; source caps and outer silhouette retained'}


def save_spacing_review(original, refined, destination):
    sheet = Image.new('RGB', (1320, 820), '#e9edf1')
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 20), 'Family seam spacing / compare at equal visible width', font=label_font(27), fill=NAVY)
    with Image.open(REFERENCE) as source:
        reference = source.crop(source.getchannel('A').getbbox())
    options = [('WoW2 / before', colorize(original, NAVY), 'About 3% of visible width'),
               ('WoW2 / applied', colorize(refined, NAVY), '1/24 of visible width (4.17%)'),
               ('Wheelhouse / reference', reference, 'About 4% of visible width')]
    for column, (label, asset, note) in enumerate(options):
        left = 16 + column * 436
        draw.rounded_rectangle((left, 78, left + 420, 746), radius=12, fill='#ffffff')
        draw.text((left + 18, 96), label, font=label_font(25), fill=NAVY)
        draw.text((left + 18, 132), note, font=label_font(19), fill=NAVY)
        width = 360
        mark = asset.resize((width, round(asset.height * width / asset.width)), Image.Resampling.LANCZOS)
        sheet.paste(mark, (left + 30, 186 + (280 - mark.height) // 2), mark)
        for row, size in enumerate((24, 32, 48)):
            top = 505 + row * 76
            draw.text((left + 20, top), f'{size}px wide', font=label_font(18), fill=NAVY)
            small = asset.resize((size, round(asset.height * size / asset.width)), Image.Resampling.LANCZOS)
            sheet.paste(small, (left + 140, top), small)
            enlarged = small.resize((small.width * 3, small.height * 3), Image.Resampling.NEAREST)
            sheet.paste(enlarged, (left + 230, top - 8), enlarged)
    draw.text((24, 774), 'Facing seam bodies share a visual weight. Rounded tips and junctions retain their own geometry.',
              font=label_font(20), fill=NAVY)
    sheet.save(destination / 'seam-spacing-review.png')


def pad(image):
    result = Image.new('RGBA', (image.width + PADDING * 2, image.height + PADDING * 2))
    result.alpha_composite(image, (PADDING, PADDING))
    return result


def fit_height(image, height):
    if height > image.height:
        raise ValueError('This exporter does not upscale raster artwork')
    width = round(image.width * height / image.height)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def primary(symbol, lettering):
    mark = fit_height(symbol, 176)
    name = fit_height(lettering, 146)
    gap = 44
    result = Image.new('RGBA', (mark.width + gap + name.width, mark.height))
    result.alpha_composite(mark)
    result.alpha_composite(name, (mark.width + gap, (mark.height - name.height) // 2))
    return pad(result)


def tile(symbol):
    size, scale = 384, 4
    mask = Image.new('L', (size * scale, size * scale))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * scale - 1, size * scale - 1),
                                           radius=80 * scale, fill=255)
    base = colorize(mask.resize((size, size), Image.Resampling.LANCZOS), NAVY)
    width = 272
    mark = symbol.resize((width, round(symbol.height * width / symbol.width)), Image.Resampling.LANCZOS)
    base.alpha_composite(mark, ((size - mark.width) // 2, (size - mark.height) // 2))
    return pad(base)


def micro_alpha(alpha, canvas_size):
    """Open only touching panel seams at a fixed pixel size; retain source contours."""
    parts = []
    source = np.asarray(alpha)
    for group in components(source >= 128):
        mask = np.zeros(source.shape, dtype=np.uint8)
        xs, ys = zip(*group)
        mask[ys, xs] = 255
        band = np.asarray(Image.fromarray(mask).filter(ImageFilter.MaxFilter(5))) > 0
        parts.append(Image.fromarray(np.where(band, source, 0).astype(np.uint8)))
    width = canvas_size - 2
    size = (width, round(alpha.height * width / alpha.width))
    scaled = np.stack([np.asarray(part.resize(size, Image.Resampling.LANCZOS)) for part in parts])
    owner = scaled.argmax(axis=0)
    result = np.array(alpha.resize(size, Image.Resampling.LANCZOS))
    clear = np.zeros(result.shape, dtype=bool)
    for y in range(size[1]):
        for x in range(size[0]):
            for nx, ny in ((x + 1, y), (x, y + 1)):
                if nx >= size[0] or ny >= size[1]:
                    continue
                if result[y, x] >= 32 and result[ny, nx] >= 32 and owner[y, x] != owner[ny, nx]:
                    if scaled[owner[y, x], y, x] < scaled[owner[ny, nx], ny, nx]:
                        clear[y, x] = True
                    else:
                        clear[ny, nx] = True
    result[clear] = 0
    count = len(components(result >= 128, minimum=1))
    if count != 3:
        raise ValueError(f'Micro {canvas_size}px did not retain three separate panels')
    canvas = Image.new('L', (canvas_size, canvas_size))
    canvas.paste(Image.fromarray(result), (1, (canvas_size - size[1]) // 2))
    return canvas, {'canvas_px': canvas_size, 'symbol_width_px': width,
                    'components_alpha_128': count, 'seam_pixels_cleared': int(clear.sum())}


def save_micro_review(symbols, exports, destination):
    sheet = Image.new('RGB', (1120, 750), '#e9edf1')
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 20), 'Panels / optical micro derivatives / fixed-size exports', font=label_font(26), fill=NAVY)
    for row, (suffix, dark) in enumerate((('navy', False), ('white', True))):
        top = 80 + row * 310
        draw.rectangle((16, top, 1104, top + 290), fill='#142033' if dark else '#ffffff')
        ink = '#ffffff' if dark else NAVY
        for column, size in enumerate((16, 24)):
            x = 40 + column * 540
            draw.text((x, top + 16), f'{size}px canvas / standard -> optical', font=label_font(20), fill=ink)
            width = size - 2
            mark = symbols[suffix].resize((width, round(symbols[suffix].height * width / symbols[suffix].width)),
                                           Image.Resampling.LANCZOS)
            standard = Image.new('RGBA', (size, size))
            standard.alpha_composite(mark, (1, (size - mark.height) // 2))
            optical = exports[f'wow2-symbol-micro-{size}-{suffix}.png']
            for offset, asset in ((0, standard), (230, optical)):
                sheet.paste(asset, (x + offset, top + 55), asset)
                enlarged = asset.resize((size * 7, size * 7), Image.Resampling.NEAREST)
                sheet.paste(enlarged, (x + offset, top + 94), enlarged)
    draw.text((24, 716), 'Actual size above; 7x pixel enlargement below. Use these only at their named sizes.',
              font=label_font(18), fill=NAVY)
    sheet.save(destination / 'micro-review.png')


def label_font(size=21):
    # Pillow's bundled font keeps review sheets independent of host font installs.
    return ImageFont.load_default(size=size)


def save_preview(exports, destination):
    sheet = Image.new('RGB', (1400, 1060), '#e9edf1')
    draw = ImageDraw.Draw(sheet)
    font = label_font()
    draw.text((32, 24), 'WoW2 / Panels / canonical raster family', font=label_font(28), fill=NAVY)
    layout = [
        ('wow2-primary-navy.png', 'Primary / light', (24, 82, 690, 330), False),
        ('wow2-primary-white.png', 'Primary / dark', (710, 82, 1376, 330), True),
        ('wow2-symbol-navy.png', 'Symbol / light', (24, 350, 462, 670), False),
        ('wow2-symbol-white.png', 'Symbol / dark', (482, 350, 920, 670), True),
        ('wow2-tile.png', 'Tile / avatar and launcher', (940, 350, 1376, 670), False),
        ('wow2-wordmark-navy.png', 'Lettering component / light', (24, 690, 690, 918), False),
        ('wow2-wordmark-white.png', 'Lettering component / dark', (710, 690, 1376, 918), True),
    ]
    for name, label, rect, dark in layout:
        x1, y1, x2, y2 = rect
        draw.rounded_rectangle(rect, radius=12, fill='#142033' if dark else '#ffffff')
        draw.text((x1 + 20, y1 + 16), label, font=font, fill='#dbe5f1' if dark else NAVY)
        asset = exports[name].copy()
        asset.thumbnail((x2 - x1 - 72, y2 - y1 - 96), Image.Resampling.LANCZOS)
        sheet.paste(asset, (x1 + (x2 - x1 - asset.width) // 2,
                           y1 + 60 + (y2 - y1 - 80 - asset.height) // 2), asset)
    draw.text((32, 956), 'Panels shape; refined family seam spacing; transparent gaps.', font=font, fill=NAVY)
    draw.text((32, 992), 'Raster exports from the approved source. Editable vector masters remain separate work.',
              font=label_font(18), fill=NAVY)
    sheet.save(destination / 'preview.png')


def save_size_review(symbols, primaries, app_tile, destination):
    sheet = Image.new('RGB', (1040, 800), '#e9edf1')
    draw = ImageDraw.Draw(sheet)
    font = label_font(18)
    draw.text((24, 18), 'WoW2 / actual pixel-size review (inspect at 100%)', font=label_font(25), fill=NAVY)
    metrics = []
    for row, (suffix, dark) in enumerate((('navy', False), ('white', True))):
        top = 68 + row * 266
        background = '#142033' if dark else '#ffffff'
        ink = '#ffffff' if dark else NAVY
        draw.rectangle((16, top, 1024, top + 246), fill=background)
        symbol = symbols[suffix]
        for column, width in enumerate((16, 20, 24, 32, 48, 64)):
            x = 36 + column * 150
            draw.text((x, top + 16), f'{width}px wide', font=font, fill=ink)
            mark = symbol.resize((width, round(symbol.height * width / symbol.width)), Image.Resampling.LANCZOS)
            sheet.paste(mark, (x, top + 55), mark)
            count = len(components(np.array(mark.getchannel('A')) >= 128, minimum=1))
            metrics.append({'surface': suffix, 'symbol_width_px': width,
                            'symbol_height_px': mark.height, 'components_alpha_128': count})
        for column, height in enumerate((24, 32, 40, 48)):
            x = 36 + column * 240
            draw.text((x, top + 137), f'Primary {height}px high', font=font, fill=ink)
            logo = fit_height(primaries[suffix], height)
            sheet.paste(logo, (x, top + 172), logo)
    draw.rectangle((16, 600, 1024, 784), fill='#ffffff')
    for column, size in enumerate((48, 64, 96)):
        x = 36 + column * 320
        draw.text((x, 614), f'Tile {size}px', font=font, fill=NAVY)
        asset = app_tile.resize((size, size), Image.Resampling.LANCZOS)
        sheet.paste(asset, (x, 652), asset)
    sheet.save(destination / 'size-review.png')
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=BRAND)
    args = parser.parse_args()
    if digest(SOURCE) != SOURCE_SHA256:
        parser.error('Approved source checksum changed; review before re-exporting')
    if digest(REFERENCE) != REFERENCE_SHA256:
        parser.error('Wheelhouse comparison source checksum changed; review before re-exporting')
    source = Image.open(SOURCE).convert('RGB')
    if source.size != (1254, 1254):
        parser.error('Expected the approved 1254x1254 Panels card')
    original_alpha, mark_metadata = extract_alpha(source, (250, 250, 1010, 790), 3)
    mark_alpha, seam_metadata = harmonize_seams(original_alpha)
    name_alpha, name_metadata = extract_alpha(source, (260, 800, 1040, 1000), 4)
    destination = args.output_dir.expanduser().resolve()
    output = destination / 'panels'
    output.mkdir(parents=True, exist_ok=True)
    exports, symbols, primaries = {}, {}, {}
    for suffix, color in (('navy', NAVY), ('white', WHITE)):
        symbols[suffix] = colorize(mark_alpha, color)
        name = colorize(name_alpha, color)
        primaries[suffix] = primary(symbols[suffix], name)
        exports[f'wow2-primary-{suffix}.png'] = primaries[suffix]
        exports[f'wow2-symbol-{suffix}.png'] = pad(symbols[suffix])
        exports[f'wow2-wordmark-{suffix}.png'] = pad(name)
    exports['wow2-tile.png'] = tile(symbols['white'])
    micro_metrics = []
    for size in (16, 24):
        alpha, metric = micro_alpha(mark_alpha, size)
        micro_metrics.append(metric)
        for suffix, color in (('navy', NAVY), ('white', WHITE)):
            exports[f'wow2-symbol-micro-{size}-{suffix}.png'] = colorize(alpha, color)
    assets = []
    for name, asset in exports.items():
        path = output / name
        asset.save(path, optimize=True)
        alpha = np.asarray(asset.getchannel('A'))
        if any(np.any(edge) for edge in (alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1])):
            raise ValueError(f'Nontransparent export border: {name}')
        assets.append({'file': 'panels/' + name, 'width': asset.width, 'height': asset.height,
                       'alpha_bbox': list(asset.getchannel('A').getbbox()), 'sha256': digest(path)})
    save_preview(exports, destination)
    small_sizes = save_size_review(symbols, primaries, exports['wow2-tile.png'], destination)
    save_micro_review(symbols, exports, destination)
    save_spacing_review(original_alpha, mark_alpha, destination)
    manifest = {'schema': 1, 'identity': 'wow2-panels', 'approved': '2026-09-29',
                'source': {'file': 'source/panels-approved.png', 'sha256': SOURCE_SHA256},
                'comparison_source': {'file': 'source/wheelhouse-gap-reference.png',
                                      'sha256': REFERENCE_SHA256},
                'seam_refinement': seam_metadata,
                'raster_only': True, 'colors': {'navy': '#23324f', 'white': '#ffffff'},
                'extraction': {'symbol': mark_metadata, 'lettering': name_metadata},
                'composition': {'symbol_height': 176, 'lettering_height': 146, 'gap': 44,
                                'export_padding': PADDING, 'tile_content_width': 272},
                'micro': {'status': 'included in the approved final export family', 'fixed_pixel_sizes': [16, 24],
                          'method': 'clear weaker touching seam pixels; no outer-contour redraw',
                          'metrics': micro_metrics},
                'assets': assets, 'small_size_metrics': small_sizes}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'assets': assets, 'small_size_metrics': small_sizes}, indent=2))


if __name__ == '__main__':
    main()
