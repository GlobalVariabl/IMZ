import sys


def parse_config_file(file_name: str) -> dict:
    redict = {}
    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                if "=" not in line:
                    raise ValueError(f"the line ({line}) is not valid")
                key, value = line.split("=", 1)
                redict[key.strip().upper()] = value.strip()
    except ValueError as e:
        print("ERROR:", e)
        return None
    return redict


def get_location(string_loc: str) -> tuple:
    try:
        x, y = string_loc.split(",", 1)
        return (int(x), int(y))
    except Exception:
        raise ValueError("invalid location value")


def check_locations_within_eria(location: tuple, wigth: int,
                                height: int) -> bool:
    if 0 <= location[0] < wigth and 0 <= location[1] < height:
        return (True)
    return (False)


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    configs = parse_config_file(sys.argv[1])

    try:
        wigth = int(configs["WIDTH"])
        height = int(configs["HEIGHT"])
        entry = get_location(configs["ENTRY"])
        exit = get_location(configs["EXIT"])
        output_file = int(configs["OUTPUT_FILE"])
        perfect = (configs.get("PERFECT".lower(), "true") == "true")
        seed = int(configs["SEED"] if "SEED" in configs.keys() else None)

    except ValueError as e:
        print(f"EROOR: invalid value in config ({e})")
    except KeyError:
        print("ERROR: there is not key in configfile")

    if not check_locations_within_eria(entry, wigth, height):
        print("ENTRY point is outsid of the maze")
        sys.exit(1)
    if not check_locations_within_eria(exit, wigth, height):
        print("EXIT point is outsid of the maze")
        sys.exit(1)
    if entry[0] == exit[0] and entry[1] == exit[1]:
        print("ENTRY and EXIT points can not be the same point")
        sys.exit(0)


if __name__ == "__main__":
    main()
