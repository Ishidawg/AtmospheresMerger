import configparser
import os
import shutil

merge_file: str = "/home/ishidaw/.local/share/Steam/steamapps/common/Dark Souls II Scholar of the First Sin/Game/ds2le_atmosphere_presets/atmospheres_extended.ini"
into_file: str = "/home/ishidaw/Games/Mods/Fromsoftware/DS2/atmospheres_extended_original_test.ini"
test_file: str = "/home/ishidaw/Games/Mods/Fromsoftware/DS2/test.ini"


def backup_atmospheres(game_path: str) -> None:
    backup: str = f"{game_path}.bak"
    shutil.copy2(game_path, backup)


def merge_atmospheres(game_path: str, community_path: str) -> None:
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
        if section == "Atmosphere_Triggers":
            continue

        if game_config.has_section(section):
            game_config.remove_section(section)

        game_config.add_section(section)

        for key, value in community_config.items(section):
            game_config.set(section, key, value)

    with open(game_path, "w", encoding='utf-8') as file:
        game_config.write(file, space_around_delimiters=False)


if __name__ == "__main__":
    game_file: str = "/home/ishidaw/.local/share/Steam/steamapps/common/Dark Souls II Scholar of the First Sin/Game/ds2le_atmosphere_presets/atmospheres_extended.ini"
    community_file: str = "/home/ishidaw/Games/Mods/Fromsoftware/DS2/atmospheres_extended_community.ini"

    merge_atmospheres(game_file, community_file)
