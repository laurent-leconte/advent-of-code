# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow",
# ]
# ///

from itertools import combinations
from pathlib import Path

from PIL import Image, ImageDraw

from utils import read_input
from itertools import pairwise

def points() -> list[tuple[int, int]]:
    raw_lines = read_input(day=9)
    pts = []
    for line in raw_lines:
        x_str, y_str = line.split(",")
        x, y = int(x_str), int(y_str)
        pts.append((x, y))
    return pts

def squish(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    xs, ys = zip(*points)
    x_idx = {x: i for i, x in enumerate(sorted(set(xs)))}
    y_idx = {y: i for i, y in enumerate(sorted(set(ys)))}
    return [(x_idx[x], y_idx[y]) for x, y in points]


def make_image(edges, rectangle=None, outside_points=None, filename: str | None = None) -> None:
    """ Draw the lines between points and save as an image."""
    
    if len(edges) < 2:
        print("Not enough points to draw.")
        return

    edges.append(edges[0])  # Close the loop
    xs, ys = zip(*edges)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max_x - min_x
    span_y = max_y - min_y

    # Keep the generated image reasonably sized regardless of the coordinate range.
    target_pixels = 1800
    max_span = max(span_x, span_y, 1)
    scale = max_span / target_pixels if max_span > target_pixels else 1.0

    padding = 20
    img_width = max(1, int(round(span_x / scale)) + padding * 2)
    img_height = max(1, int(round(span_y / scale)) + padding * 2)
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    def transform(point: tuple[int, int]) -> tuple[int, int]:
        x, y = point
        sx = int(round((x - min_x) / scale)) + padding
        sy = int(round((y - min_y) / scale)) + padding
        return sx, sy

    scaled_points = [transform(p) for p in edges]
    line_width = 1
    draw.line(scaled_points, fill="black", width=line_width)

    if rectangle:
        rx1, ry1, rx2, ry2 = rectangle
        sp1 = transform((rx1, ry1))
        sp2 = transform((rx2, ry2))
        draw.rectangle([sp1, sp2], outline="red", width=line_width)

    if outside_points:
        for op in outside_points:
            sx, sy = transform(op)
            img.putpixel((sx, sy), (0, 200, 200))

    if filename:
        output_path = Path(filename).with_suffix(".png")
    else:
        output_path = Path(__file__).with_suffix(".png")
    img.save(output_path)
    print(f"Saved image to {output_path} with scale factor {scale:.2f}.")


def visualize() -> None:
    original_points = points()
    make_image(original_points, "original")
    squished_points = squish(original_points)
    make_image(squished_points, "squished")


def day9() -> int:
    """
    Idea:
    * Convert to compacted coordinates
    * build a set of all points *not* in polygon
        * build the polygon point by point
        * flood fill the outside area
    * generate all possible rectangles (sorted by area)
    * for part1, return the largest area
    * for part2:
        * for each rectangle, check if any point in the perimeter is outside the polygon
        * if not, return area
    
    :return: Description
    :rtype: int
    """
    original_points = points()
    xs, ys = zip(*original_points)
    # work with compacted coordinates (still preserving inside/outside information)
    x_idx = {x: i for i, x in enumerate(sorted(set(xs)))}
    y_idx = {y: i for i, y in enumerate(sorted(set(ys)))}
    squished = [(x_idx[x], y_idx[y]) for x, y in original_points]
    max_x, max_y = len(x_idx), len(y_idx)

    # Build a set of all points outside the polygon
    polygon = set()
    for p1, p2 in pairwise(squished + [squished[0]]):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                polygon.add((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                polygon.add((x, y1))
        else:
            raise ValueError("Only axis-aligned edges are supported.")
    outside = set()
    to_visit = [(0, 0), (max_x - 1, 0), (0, max_y - 1), (max_x - 1, max_y - 1)]
    while to_visit:
        x, y = to_visit.pop()
        if (x, y) in outside or (x, y) in polygon:
            continue
        outside.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_x and 0 <= ny < max_y:
                to_visit.append((nx, ny))
    # make_image(squished, outside, "part2_filled")

    # Generate all possible rectangles, sorted by area (largest first)
    all_rectangles = []
    for p1, p2 in combinations(original_points, 2):
        x1, y1 = p1
        x2, y2 = p2
        rx1, ry1 = min(x1, x2), min(y1, y2)
        rx2, ry2 = max(x1, x2), max(y1, y2)
        area = (rx2 - rx1 + 1) * (ry2 - ry1 + 1)
        all_rectangles.append((area, (rx1, ry1, rx2, ry2)))
    part1_solution, part1_rectangle = max(all_rectangles, key=lambda x: x[0])
    make_image(original_points, part1_rectangle, None, "part1_solution")
    print("Part 1:", part1_solution)
    for area, (rx1, ry1, rx2, ry2) in sorted(all_rectangles, reverse=True):
        # Check if any point on the perimeter is outside the polygon
        perimeter_outside = False
        squished_rx1, squished_ry1 = x_idx[rx1], y_idx[ry1]
        squished_rx2, squished_ry2 = x_idx[rx2], y_idx[ry2]
        for x in range(squished_rx1, squished_rx2 + 1):
            for y in (squished_ry1, squished_ry2):
                if (x, y) in outside:
                    perimeter_outside = True
                    break
            if perimeter_outside:
                break
        if perimeter_outside:
            continue
        for y in range(squished_ry1 + 1, squished_ry2):
            for x in (squished_rx1, squished_rx2):
                if (x, y) in outside:
                    perimeter_outside = True
                    break
            if perimeter_outside:
                break
        if not perimeter_outside:
            # Found the largest rectangle fully inside the polygon
            make_image(original_points, (rx1, ry1, rx2, ry2), None, "part2_solution")
            print("Part 2:", area)
            break


if __name__ == '__main__':
    # visualize()
    day9()