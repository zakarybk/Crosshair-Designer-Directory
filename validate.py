from parse import crosshair_configs

configs = crosshair_configs()


def is_valid_size(crosshair):
    # Where max value is 3 digits + space
    # Overestimate of actual length by a lot
    return (
        len(crosshair) < (len(configs) * 3+1)
        and len(crosshair.split(' ')) <= len(configs)
    )


def load_raw_crosshair(crosshair):
    if not is_valid_size(crosshair):
        raise Exception('Crosshair payload too large!')

    valid_settings = ''
    settings = crosshair.split(' ')
