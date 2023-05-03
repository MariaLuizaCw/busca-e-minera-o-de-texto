def read_config_file(file, config_dict):
    with open(file, "r") as config:
        for line in config:
            key = line.split('=')[0]
            value = line.split('=')[1].replace('\n', '')
            if key in config_dict.keys():
                config_dict[key].append(value)
            else:
                config_dict[key] = [value]