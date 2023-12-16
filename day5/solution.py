SEED_HEADER = "seeds:"
SEED_TO_SOIL_MAP_HEADER = "seed-to-soil map:"
SEED_TO_FERTILIZER_MAP_HEADER = "soil-to-fertilizer map:"
FERTILIZER_TO_WATER_MAP_HEADER = "fertilizer-to-water map:"
WATER_TO_LIGHT_MAP_HEADER = "water-to-light map:"
LIGHT_TO_TEMPERATURE_MAP_HEADER = "light-to-temperature map:"
TEMPERATURE_TO_HUMIDITY_MAP_HEADER = "temperature-to-humidity map:"
HUMIDITY_TO_LOCATION_MAP_HEADER = "humidity-to-location map:"


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def extract_seeds(lines: list[str]) -> list[int]:
    seed_line = lines[0]
    seed_line = seed_line.replace(SEED_HEADER, "")
    seeds = seed_line.split()
    seeds = [int(num) for num in seeds]
    return seeds


def extract_seeds_part_two(lines: list[str]) -> list[int]:
    seed_line = lines[0]
    seed_line = seed_line.replace(SEED_HEADER, "").strip()
    seeds_parts = seed_line.split()

    if len(seeds_parts) % 2 != 0:
        raise ValueError("Seed parts should be in pairs")

    seeds = [seed for start, length in zip(seeds_parts[::2], seeds_parts[1::2])
             for seed in range(int(start), int(start) + int(length))]

    return seeds


class CustomMap:
    def __init__(self, destination_start, source_start, mapping_range):
        self.destination_start = destination_start
        self.source_start = source_start
        self.mapping_range = mapping_range

    def get_destination_range(self):
        return range(self.destination_start, self.destination_start + self.mapping_range)

    def get_destination_number(self, source_number):
        if source_number < self.source_start or source_number >= self.source_start + self.mapping_range:
            raise ValueError("Source number is out of the mapping range.")
        offset = source_number - self.source_start
        return self.destination_start + offset


def parse_lit_to_custom_mappers(list: list[str]) -> list[CustomMap]:
    custom_maps = []

    for line in list:
        parts = line.split()
        if len(parts) != 3:
            print("Error on line: " + line)
            raise ValueError("Each line must contain exactly three numbers.")

        destination_start, source_start, mapping_range = map(int, parts)
        custom_map = CustomMap(destination_start, source_start, mapping_range)
        custom_maps.append(custom_map)

    return custom_maps


def part_one(lines: list[str]) -> None:
    seeds = extract_seeds_part_two(lines)

    seed_to_soil_str_list = []
    seed_to_fertilizer_str_list = []
    fertilizer_to_water_str_list = []
    water_to_light_str_list = []
    light_to_temperature_str_list = []
    temperature_to_humidity_str_list = []
    humidity_to_location_str_list = []

    current_map = None

    for line in lines[1:]:
        if len(line) == 0:
            current_map = None
            continue
        elif line.startswith(SEED_HEADER):
            current_map = None
            continue
        elif line == SEED_TO_SOIL_MAP_HEADER:
            current_map = seed_to_soil_str_list
        elif line == SEED_TO_FERTILIZER_MAP_HEADER:
            current_map = seed_to_fertilizer_str_list
        elif line == FERTILIZER_TO_WATER_MAP_HEADER:
            current_map = fertilizer_to_water_str_list
        elif line == WATER_TO_LIGHT_MAP_HEADER:
            current_map = water_to_light_str_list
        elif line == LIGHT_TO_TEMPERATURE_MAP_HEADER:
            current_map = light_to_temperature_str_list
        elif line == TEMPERATURE_TO_HUMIDITY_MAP_HEADER:
            current_map = temperature_to_humidity_str_list
        elif line == HUMIDITY_TO_LOCATION_MAP_HEADER:
            current_map = humidity_to_location_str_list

        current_map.append(line)

    seeds_to_soil = parse_lit_to_custom_mappers(seed_to_soil_str_list[1:])
    seed_to_fertilizer = parse_lit_to_custom_mappers(
        seed_to_fertilizer_str_list[1:])
    fertilizer_to_water = parse_lit_to_custom_mappers(
        fertilizer_to_water_str_list[1:])
    water_to_light = parse_lit_to_custom_mappers(water_to_light_str_list[1:])
    light_to_temperature = parse_lit_to_custom_mappers(
        light_to_temperature_str_list[1:])
    temperature_to_humidity = parse_lit_to_custom_mappers(
        temperature_to_humidity_str_list[1:])
    humidity_to_location = parse_lit_to_custom_mappers(
        humidity_to_location_str_list[1:])

    lowest_location = float('inf')

    for seed in seeds:
        current_value = seed
        for mapping in [seeds_to_soil, seed_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location]:
            for custom_map in mapping:
                if custom_map.source_start <= current_value < custom_map.source_start + custom_map.mapping_range:
                    current_value = custom_map.get_destination_number(
                        current_value)
                    break
            else:
                break
        else:
            lowest_location = min(lowest_location, current_value)

    lowest_location if lowest_location != float('inf') else None
    print(f"Lowest location:", lowest_location)


if __name__ == '__main__':
    lines = read_lines_of_file("./text.txt")
    part_one(lines)
