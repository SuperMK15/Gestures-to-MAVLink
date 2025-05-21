import yaml

def load_drone_config(config_path="./configs/drone.yaml"):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config["drone"]
