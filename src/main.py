__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2024. All rights reserved."

from src.web.api import app
from src.web.configparams import configuration_parameters


if __name__ == '__main__':
    import uvicorn

    port_num = int(configuration_parameters['port'])
    host = configuration_parameters['host']
    log_level = configuration_parameters['log_level']
    uvicorn.run(app, host='0.0.0.0', port=port_num, log_level="debug")
