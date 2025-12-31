import yaml
import csv
import random
from pathlib import Path

# ==============================
# Configuration
# ==============================

CONFIG_PATH = "generator_config.yaml"

# ==============================
# Load Generator Config
# ==============================

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

gen_cfg = config["generation"]
tools_cfg = config["tools"]

ROWS_PER_TOOL = gen_cfg["rows_per_tool"]
MIN_CMDS = gen_cfg["min_commands"]
MAX_CMDS = gen_cfg["max_commands"]
OUTPUT_FILE = gen_cfg["output_file"]

TARGET_POOL = gen_cfg["pools"]["targets"]
URL_POOL = gen_cfg["pools"]["urls"]

# ==============================
# Helper Functions
# ==============================

def render_command_list(templates):
    """
    Generate a tab + space delimited command list (25–40 commands)
    """
    num_cmds = random.randint(MIN_CMDS, MAX_CMDS)

    chosen_templates = random.sample(
        templates,
        min(len(templates), num_cmds)
    )

    commands = []
    for tpl in chosen_templates:
        cmd = tpl.format(
            target=random.choice(TARGET_POOL),
            url=random.choice(URL_POOL)
        )
        commands.append(cmd)

    # IMPORTANT FIX: tab + space delimiter
    return "\t ".join(commands)

# ==============================
# CSV Generation
# ==============================

Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)

total_rows_written = 0

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # CSV HEADER (AUTHORITATIVE)
    writer.writerow([
        "command_list",
        "tool",
        "mitre_stage",
        "intent",
        "category"
    ])

    # One tool at a time (HARD GUARANTEE: 5000 rows per tool)
    for tool in tools_cfg:
        tool_name = tool["name"]
        mitre_stage = tool["mitre_stage"]
        intents = tool["intents"]

        tool_row_count = 0

        while tool_row_count < ROWS_PER_TOOL:
            intent_block = random.choice(intents)

            command_list = render_command_list(
                intent_block["templates"]
            )

            writer.writerow([
                command_list,
                tool_name,
                mitre_stage,
                intent_block["intent"],
                intent_block["category"]
            ])

            tool_row_count += 1
            total_rows_written += 1

        print(f"[+] Generated {ROWS_PER_TOOL} rows for tool: {tool_name}")

print("=" * 60)
print(f"[✓] DATASET COMPLETE")
print(f"[✓] Total rows written: {total_rows_written}")
print(f"[✓] Output file: {OUTPUT_FILE}")
print("=" * 60)
