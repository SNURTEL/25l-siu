from dataclasses import dataclass

from PIL import Image, ImageDraw

PX_IN_METER = 22
COLORS = ["red", "green", "blue", "orange", "purple", "cyan", "magenta"]


@dataclass
class Section:
    top_left: tuple[int, int]
    bottom_right: tuple[int, int]
    dest: tuple[int, int]


def draw_section(
    section: Section,
    draw_context: ImageDraw.ImageDraw,
    color: str = "red",
) -> None:
    draw_context.rectangle([section.top_left, section.bottom_right], outline=color, width=5)
    radius = 8
    x, y = section.dest
    draw_context.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)


def get_section_definition(
    section: Section,
    num_of_agents: int,
) -> str:
    x_min = section.top_left[0]
    x_max = section.bottom_right[0]

    y_min = 1080 - section.bottom_right[1]
    y_max = 1080 - section.top_left[1]

    target_x = section.dest[0]
    target_y = 1080 - section.dest[1]

    data = [x_min, x_max, y_min, y_max, target_x, target_y]
    data = [f"{(value / PX_IN_METER):.3f}" for value in data]
    data = [1, num_of_agents] + data
    data = [str(element) for element in data]
    return ";".join(data)


if __name__ == "__main__":
    sections = [
        Section((480, 460), (640, 600), (730, 710)),
        Section((804, 727), (885, 863), (1100, 781)),
        Section((1527, 476), (1665, 672), (1189, 450)),
        Section((1058, 224), (1200, 428), (790, 125)),
        Section((500, 80), (730, 180), (385, 360)),
    ]
    num_of_agents = 2

    img = Image.open("roads_multi.png")
    draw_context = ImageDraw.Draw(img)
    csv_string = ""
    for idx, section in enumerate(sections):
        color = COLORS[idx % (len(COLORS))]
        draw_section(section, draw_context, color)
        csv_string += get_section_definition(section, num_of_agents)
        csv_string += "\n"
    img.save("roads_multi_scenario.png")
    with open("routes_multi.csv", "w") as f:
        f.write(csv_string)
