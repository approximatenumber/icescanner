# example with configuration

import yaml
from icescanner.algo.input_filter import is_dataset_valid

# Read configuration file
config_file = "/opt/icescanner/config.yml"
config = yaml.load(open(config_file).read(), Loader=yaml.FullLoader)

# Dataset filepath
dataset_file = "/opt/datasets/port_lidar/2021-03-01_12-00-00.csv"

# Run input filter algorithm
is_valid = is_dataset_valid(dataset_file, config=config)
print(is_valid)
