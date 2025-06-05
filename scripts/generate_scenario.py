from dataclasses import dataclass
from typing import List
from PIL import Image, ImageDraw, ImageFont

PX_IN_METER = 22
COLORS = ["red", "green", "blue", "orange", "purple", "cyan", "magenta"]


@dataclass
class Section:
    top_left: tuple[int, int]
    bottom_right: tuple[int, int]
    dest: tuple[int, int]

@dataclass
class Scenario:
    sections: List[Section]
    num_of_agents: int

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

    center_x = (section.top_left[0] + section.bottom_right[0]) // 2
    center_y = (section.top_left[1] + section.bottom_right[1]) // 2

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    text = str(number)
    draw_context.text((center_x, center_y), text, fill=color, font=font, anchor="mm")


def draw_scenario(
    scenario: Scenario,
    draw_context: ImageDraw.ImageDraw,
    scenario_number: int,
) -> None:
    for idx, section in enumerate(scenario.sections):
        color = COLORS[idx % len(COLORS)]
        draw_section(section, draw_context, color, f"{idx + 1}")

def get_scenario_definition(
    scenario: Scenario,
    scenario_number: int,
) -> str:
    csv_lines = []
    for section in scenario.sections:
        x_min = section.top_left[0]
        x_max = section.bottom_right[0]
        y_min = 1080 - section.bottom_right[1]
        y_max = 1080 - section.top_left[1]
        target_x = section.dest[0]
        target_y = 1080 - section.dest[1]
        
        data = [x_min, x_max, y_min, y_max, target_x, target_y]
        data = [f"{(value / PX_IN_METER):.3f}" for value in data]
        data = [scenario_number, scenario.num_of_agents] + data
        csv_lines.append(";".join(map(str, data)))
    return "\n".join(csv_lines)


if __name__ == "__main__":
    scenarios = [
        Scenario(
            sections=[
                Section((1267, 458), (1458, 584), (1152, 362)),
                Section((1001, 219), (1142, 348), (782, 315)),
                Section((634, 317), (769, 486), (730, 695)),
                Section((739, 710), (917, 863), (1078, 949)),
                Section((1095, 892), (1269, 1005), (1673, 806)),
                Section((1631, 624), (1774, 795), (1491, 521)),
            ],
            num_of_agents=2
        ),
        Scenario(
            sections=[
                Section((1134, 433), (1246, 580), (859, 129)),
                Section((695, 79), (846, 178), (321, 207)),
                Section((265, 220), (439, 359), (662, 539)),
                Section((641, 561), (773, 687), (1010, 813)),
                Section((1029, 718), (1196, 835), (1196, 592)),

            ],
            num_of_agents=2
        ),
    ]

    csv_string = ""
    
    for scenario_idx, scenario in enumerate(scenarios, 1):
        img = Image.open("roads_multi.png")
        draw_context = ImageDraw.Draw(img)
        
        draw_scenario(scenario, draw_context, scenario_idx)
        
        img.save(f"roads_multi_scenario_{scenario_idx}.png")
        
        csv_string += get_scenario_definition(scenario, scenario_idx)
        csv_string += "\n"
    
    with open("routes_multi.csv", "w") as f:
        f.write(csv_string)
