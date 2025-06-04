from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

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
    number: int = 1,
) -> None:
    draw_context.rectangle([section.top_left, section.bottom_right], outline=color, width=5)
    radius = 8
    x, y = section.dest
    draw_context.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)

    # Dodanie numeru scenariusza na środku prostokąta
    center_x = (section.top_left[0] + section.bottom_right[0]) // 2
    center_y = (section.top_left[1] + section.bottom_right[1]) // 2

    # Dodanie tekstu z numerem
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Rysowanie tekstu bez białego tła
    text = str(number)
    draw_context.text((center_x, center_y), text, fill=color, font=font, anchor="mm")


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
        Section((1300, 476), (1395, 575), (1134, 333)),
        Section((1008, 225), (1083, 350), (750, 360)),
        Section((660, 400), (750, 475), (800, 775)),
        Section((825, 735), (900, 860), (1065, 956)),
        Section((1120, 900), (1195, 1000), (1660, 820)),
        Section((1662, 687), (1766, 795), (1450, 516)),
    ]
    num_of_agents = 2

    img = Image.open("roads_multi.png")
    draw_context = ImageDraw.Draw(img)
    csv_string = ""
    for idx, section in enumerate(sections):
        color = COLORS[idx % (len(COLORS))]
        draw_section(section, draw_context, color, idx + 1)  # dodano idx + 1
        csv_string += get_section_definition(section, num_of_agents)
        csv_string += "\n"
    img.save("roads_multi_scenario.png")
    with open("routes_multi.csv", "w") as f:
        f.write(csv_string)
