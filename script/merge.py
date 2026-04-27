import configparser
import os
import shutil


def backup_atmospheres(game_path: str) -> None:
    backup: str = f"{game_path}.bak"
    shutil.copy2(game_path, backup)


def merge_atmospheres(game_path: str, community_path: str, selected_selections: list[str]) -> None:
    # Safety check
    if not os.path.exists(game_path):
        raise FileNotFoundError("Game base atmosphere was not found")

    if not os.path.exists(community_path):
        raise FileNotFoundError("Cannot find community atmosphere")

    backup_atmospheres(game_path)

    game_config: configparser.ConfigParser = configparser.ConfigParser()
    community_config: configparser.ConfigParser = configparser.ConfigParser()

    # Reading
    game_config.read(game_path, encoding='utf-8')
    community_config.read(community_path, encoding='utf-8')

    for section in community_config.sections():

        # Rage says 'There will also be "Atmosphere_Triggers" section do not modify anything under this'
        if section == "Atmosphere_Triggers" or section.startswith("level_"):
            continue

        # Skips sections that is not selected
        if selected_selections is not None and section not in selected_selections:
            continue

        if game_config.has_section(section):
            game_config.remove_section(section)

        game_config.add_section(section)

        for key, value in community_config.items(section):
            game_config.set(section, key, value)

    with open(game_path, "w", encoding='utf-8') as file:
        game_config.write(file, space_around_delimiters=False)
