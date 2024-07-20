from app import run
import argparse
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Run the Flask server with specified configuration file.')
    parser.add_argument('--cfg', type=str, required=True, help='Path to the configuration file')

    args = parser.parse_args()

    config_path = args.cfg

    cfg = Config(config_path)

    run(cfg.get_server_host(), cfg.get_server_port(), debug=True)

if __name__ == '__main__':
    main()
