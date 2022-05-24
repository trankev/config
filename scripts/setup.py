import logging
import pathlib


def map_files(source_folder: pathlib.Path, destination_folder: pathlib.Path) -> None:
    for item in source_folder.iterdir():
        link_name = item.name.replace("___", ".").replace("__", "/")
        link_name = f".{link_name}"
        destination_file = destination_folder / link_name
        destination_file.parent.mkdir(parents=True, exist_ok=True)
        if destination_file.is_symlink():
            if destination_file.resolve() == item:
                logging.info("%s is already correctly set", link_name)
                continue
            logging.info("%s is currently pointing to %s, updating", link_name, destination_file.resolve())
            destination_file.unlink()
        elif destination_file.exists():
            renamed = destination_folder / f"{link_name}.old"
            logging.error("Moving existing %s to ", renamed)
            destination_file.rename(renamed)
            destination_file = destination_folder / link_name
        abspath = item.resolve()
        logging.info("Linking %s to %s", link_name, abspath)
        destination_file.symlink_to(abspath)


def link_settings() -> None:
    settings_folder = pathlib.Path(__file__).parent.parent.resolve() / "config"
    destination_folder = pathlib.Path.home()
    logging.info("Mapping files from %s to %s", settings_folder, destination_folder)
    map_files(settings_folder, destination_folder)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s][%(levelname)s] %(message)s")
    link_settings()


if __name__ == "__main__":
    main()
