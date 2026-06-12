import platform
import csv
from pathlib import Path, PurePath


def make_search_paths(root, folder):
    return PurePath.joinpath(PurePath(root), PurePath(folder))


def search_directories(path, file_name):
    paths = []
    for dir_name, sub_dirs, files in Path.walk(path):
        for file in files:
            if file.lower() == file_name:
                paths.append(PurePath.joinpath(dir_name, file))

    return paths


def by_batch(offset, all_files):
    batches = {}
    for file in all_files:
        parts = PurePath(file).parts
        building_type = parts[offset + 2]
        cz = parts[offset + 1]
        run = parts[offset + 3].split("-")
        measure = run[0]
        system_type = run[1]
        type = run[2]
        if building_type not in batches.keys():
            batches[building_type] = {}
        if measure not in batches[building_type].keys():
            batches[building_type][measure] = {}
        if system_type not in batches[building_type][measure].keys():
            batches[building_type][measure][system_type] = {}
        if type not in batches[building_type][measure][system_type].keys():
            batches[building_type][measure][system_type][type] = {}
        if cz not in batches[building_type][measure][system_type][type].keys():
            batches[building_type][measure][system_type][type][cz] = []
        batches[building_type][measure][system_type][type][cz].append(file)

    return batches


def process(batch, output_file):

    def dict_of_lists_to_list_of_dicts(d):
        # All lists must be the same length or zip will truncate
        keys = d.keys()
        values = zip(*d.values())
        return [dict(zip(keys, vals)) for vals in values]

    data_col = "Gas:Facility [J](Hourly) "

    output_data = {}
    fieldnames = []

    output_data["Date/Time"] = []
    with open(batch[0][0], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            output_data["Date/Time"].append(row["Date/Time"])
    fieldnames.append("Date/Time")

    for input_file in batch:

        output_data[input_file[0]] = []
        with open(input_file[0], newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    output_data[input_file[0]].append(row[data_col])
                except:
                    output_data[input_file[0]].append(" ")

            fieldnames.append(input_file[0])

    output = dict_of_lists_to_list_of_dicts(output_data)

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(output)


def main():

    # root of the DEER package install
    if platform.system() in ["Windows"]:
        root = "D:\\"
        search_folder = "Simulations\\"
        results_folder = PurePath("D:\\Profiles\\")
    elif platform.system() in ["Linux", "Darwin"]:
        root = "/Users/jwj/"
        search_folder = "e_plus_runs/"
        results_folder = PurePath("/Users/jwj/e_plus_results/")
    else:
        print("What, exactly, are you running this on!")
        exit()

    search_path = make_search_paths(root, search_folder)
    offset = len(PurePath(root).parts) + len(PurePath(search_folder).parts)

    # Results file_name
    # results_file_name = "instance-out.sql"
    results_file_name = "instance-var.csv"

    # Get all the results files
    all_files = search_directories(search_path, results_file_name)

    # Create batches
    batches = by_batch(offset, all_files)

    # Do each batch

    for building_type in batches.keys():
        by_building_batch = []
        print(building_type)

        output_file = PurePath.joinpath(
            results_folder,
            PurePath("gas_profile_{}.csv".format(building_type.lower())),
        )

        for measure in batches[building_type].keys():
            # print(measure)
            for system_type in batches[building_type][measure].keys():
                # print(system_type)
                for type in batches[building_type][measure][system_type].keys():
                    # print(type)
                    for cz in batches[building_type][measure][system_type][type].keys():
                        # print(cz)
                        by_building_batch.append(
                            batches[building_type][measure][system_type][type][cz]
                        )
        process(by_building_batch, output_file)


if __name__ == "__main__":
    main()
