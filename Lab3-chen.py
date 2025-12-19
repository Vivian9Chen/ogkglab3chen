import os
import re
from PIL import Image, ImageDraw

W, H = 960, 540

def read_points(path):
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = re.split(r"[,\s]+", line)
            if len(parts) < 2:
                continue
            try:
                x = int(parts[0])
                y = int(parts[1])
                pts.append((x, y))
            except ValueError:
                continue
    return pts

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def to_img(x, y):
    return x, (H - 1) - y

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    in_path = os.path.join(base_dir, "DS5.txt")
    out_img = os.path.join(base_dir, "result_hull.png")
    out_hull = os.path.join(base_dir, "DS5_hull.txt")

    pts = read_points(in_path)
    hull = convex_hull(pts)

    with open(out_hull, "w", encoding="utf-8") as f:
        for x, y in hull:
            f.write(f"{x} {y}\n")

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    r = 1
    for x, y in pts:
        if 0 <= x < W and 0 <= y < H:
            xi, yi = to_img(x, y)
            draw.rectangle([xi - r, yi - r, xi + r, yi + r], fill=(0, 0, 0))

    if len(hull) >= 2:
        poly = [to_img(x, y) for x, y in hull]
        poly.append(poly[0])
        draw.line(poly, fill=(0, 0, 255), width=2)

    img.save(out_img)

if __name__ == "__main__":
    main()

