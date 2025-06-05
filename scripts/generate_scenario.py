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
                Section((1264, 477), (1365, 582), (1118, 304)),
                Section((1008, 225), (1108, 331), (715, 379)),
                Section((657, 389), (750, 474), (802, 787)),
                Section((814, 748), (917, 863), (1078, 949)),
                Section((1090, 906), (1195, 1000), (1673, 806)),
                Section((1662, 687), (1766, 795), (1379, 524)),
            ],
            num_of_agents=2
        ),
        Scenario(
            sections=[
                Section((1073, 262), (1189, 363), (785, 120)),
                Section((645, 77), (771, 168), (329, 242)),
                Section((277, 253), (422, 340), (519, 526)),
                Section((532, 480), (629, 576), (725, 687)),
                Section((684, 698), (814, 810), (1092, 780)),
                Section((1101, 703), (1211, 800), (1158, 374)),

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
