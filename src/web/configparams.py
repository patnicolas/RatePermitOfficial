__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from typing import AnyStr, Any, Dict, Optional


class ConfigParams(object):
    def __init__(self, config_file: AnyStr):
        """
        Constructor for the test parameters CSV file
        :param config_file: Name of the test configuration file
        """
        self.config_file = config_file

    def load_config_variables(self) -> Optional[Dict[AnyStr, AnyStr]]:
        """
        Load the test variables as an option of a dictionary
        :return: Optional dictionary
        """
        try:
            with open(self.config_file, 'rt') as f:
                rows = f.read().split("\n")
                acc = {}
                for row in rows:
                    if len(row) > 0:
                        key_value = row.split(",")
                        acc[key_value[0]] = key_value[1]
            return acc
        except FileNotFoundError as e:
            print(f'ERROR: {str(e)}')
            return None
        except Exception as e:
            print(f'ERROR: {str(e)}')
            return None

    @staticmethod
    def default_config_parameters() -> Optional[Dict[AnyStr, AnyStr]]:
        configuration_util = ConfigParams('src/web/config.csv')
        return configuration_util.load_config_variables()


configuration_parameters = ConfigParams.default_config_parameters()

