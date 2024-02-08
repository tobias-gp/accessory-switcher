import asyncio
import argparse
import subprocess
import configparser
import os
import shutil
from pathlib import Path
from typing import List
import logging
import sys

BLUEUTIL_PATH = "/opt/homebrew/bin/blueutil"

class AccessorySwitcher:
    def __init__(self):
        self.devices: List[str] = []
        self.display_name: str = None
        self.sleep_time_in_s: int = 0
        self.read_config()

    def read_config(self) -> None:
        """
        Read configuration from file. Define config directory and file.
        Create config directory if it doesn't exist.
        Read config file.
        """
        config_dir = os.path.expanduser('~/.accessoryswitcher')
        config_file = os.path.join(config_dir, 'config')
        example_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config_example')

        os.makedirs(config_dir, exist_ok=True)
        if not os.path.exists(config_file):
            shutil.copyfile(example_config_file, config_file)

        config = configparser.ConfigParser()
        config.read(config_file)

        self.devices = config.get('DEFAULT', 'devices').split(',')
        self.display_name = config.get('DEFAULT', 'display_name')
        self.sleep_time_in_s = int(config.get('DEFAULT', 'sleep_time_in_s'))

        logging.info("Config file loaded")

    def is_connected(self, device: str) -> bool:
        """
        Check if a device is connected.
        """
        result = subprocess.run([BLUEUTIL_PATH, '--is-connected', device], capture_output=True, text=True)
        return result.stdout.strip() == '1'

    def connect(self, device: str) -> None:
        """
        Connect to a device if it is not already connected.
        """
        if not self.is_connected(device):
            try:
                logging.info(f"Connecting to {device}")
                result = subprocess.run([BLUEUTIL_PATH, '--connect', device], capture_output=True, text=True)
            except Exception as e:
                logging.info(f"Error connecting to {device}: {e}")

    def disconnect(self, device: str) -> None:
        """
        Disconnect from a device if it is connected.
        """
        if self.is_connected(device):
            try:
                logging.info(f"Disconnecting from {device}")
                result = subprocess.run([BLUEUTIL_PATH, '--disconnect', device], capture_output=True, text=True)
            except Exception as e:
                logging.info(f"Error disconnecting from {device}: {e}")

    async def monitor(self) -> None:
        """
        Monitor the display and connect/disconnect devices based on the display status.
        """
        config_dir = os.path.expanduser('~/.accessoryswitcher')
        config_file = os.path.join(config_dir, 'config')
        config_file_path = Path(config_file)
        last_modified_time = config_file_path.stat().st_mtime

        while True:
            current_modified_time = config_file_path.stat().st_mtime
            if current_modified_time != last_modified_time:
                self.read_config()
                last_modified_time = current_modified_time

            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).decode("utf-8")

            if self.display_name and (self.display_name in output):
                logging.info(f"{self.display_name} is connected")
                for device in self.devices:
                    self.connect(device)
            else:
                logging.info(f"{self.display_name} is not connected")
                for device in self.devices:
                    self.disconnect(device)

            await asyncio.sleep(self.sleep_time_in_s)

if __name__ == "__main__":
    # Create a logger
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)  

    # Create a stream handler that outputs to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG) 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)
    logger.info("Starting service")

    # currently, no args are needed, however, we want --help for the homebrew post install test :) 
    parser = argparse.ArgumentParser(description='Accessory Switcher: A tool to switch between devices.')
    args = parser.parse_args()

    try: 
        switcher = AccessorySwitcher()
        asyncio.run(switcher.monitor())
    except KeyboardInterrupt:
        logger.info("Exiting service")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
