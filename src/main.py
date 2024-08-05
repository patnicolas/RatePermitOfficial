from src.web.api import app
from src.web.configparams import configuration_parameters


if __name__ == '__main__':
    import uvicorn
    port_num = int(configuration_parameters['port'])
    uvicorn.run(app, host='0.0.0.0', port=port_num, log_level="debug")
