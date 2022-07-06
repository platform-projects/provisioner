import logging
import os
import sys
import configparser
import base64
import zlib

# Configure the global logging with a default logging
# level of info.

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s : %(message)s")
log_level = logging.INFO

logger = logging.getLogger("config")

config_params = { "sections" : [
                    { "name"       : "dwc", 
                      "parameters" : [ "dwc_cli", "dwc_url", "dwc_user", "dwc_password" ] },
                    { "name"       : "hana",
                      "parameters" : [ "hana_host", "hana_port", "hana_user", "hana_password", "hana_encrypt", "hana_sslverify+" ] }
                  ]
                }

config = None

def ensure_config(args):
    global log_level, config
    
    # Make sure the configuration file is present and has been initialized. The configuration
    # file is built based on the sections and parameters list above and any command line
    # arguments passed to the script.  Individual command line parameters can be passed to
    # to update individual configuration parameters.
    
    # When this routine finishs, the configuration for this session is ready for use.
    
    if args.config is None:
        config_path = os.getcwd()
        config_file = os.path.join(config_path, "config.ini")
    else:
        config_file = args.config

    config_exists = os.path.exists(config_file)
    
    if args.command != "config" and not config_exists:
        logger.critical("Configuration file not found - please use the config command.")
        sys.exit(1)

    config = configparser.ConfigParser()
    write_config = False
    
    if config_exists:
      config.read(config_file)
    
    for section in config_params["sections"]:
      # Make sure the section is present.
      if section["name"] not in config:
        config[section["name"]] = {}
        write_config = True
      
      # Check for mandatory parameter - traling '+' means optional
      
      for parameter in section["parameters"]:
        if parameter[-1] == '+':
          param_name = parameter[:-1]
          required = False
        else:
          param_name = parameter
          required = True
        
        # If the parameter is on the command line, assign the value
        # to the configuration.
            
        if param_name in vars(args): # Was the parameter on the command line?
          param_value = str(vars(args)[param_name])
          
          if param_name.find("password") == -1:
            config[section["name"]][param_name] = param_value
          else:
            config[section["name"]][param_name] = fn_blur(param_value)
            
          write_config = True
        
        # Last step: make sure required parameters have been
        # configured.
          
        if param_name not in config[section["name"]]:
          if required:
            logger.error(f"required configuration parameter {param_name} has no value.")
            
    if write_config:
      with open(config_file, 'w') as config_handle:
        config.write(config_handle)
      
    # Figure out the logging level - default is info.

    if args.logging is not None:
        if args.logging == "info":
            logger.setLevel(logging.INFO)
            logger.info("Logging set to INFO")
        else:
            logger.setLevel(logging.DEBUG)
            logger.info("Logging set to DEBUG")

    # Set the level so subsequent commands can set their
    # level to match.

    log_level = logger.getEffectiveLevel()

def get_config_param(section, parameter):
  if config is None:
    logger.error("get_config_param: configuration has not been initialized.")
    return
  
  param_value = config[section][parameter]
  
  if parameter.find("password") == -1:
    return param_value
  else:
    return fn_unblur(param_value)

def fn_blur(value):
    value_b = str.encode(value)
    value_b64 = base64.b64encode(value_b)
    value_z = zlib.compress(value_b64)
    value_z_b64 = base64.b64encode(value_z)
    
    return str(value_z_b64, 'UTF-8')

def fn_unblur(value_z_b64):
    value_z = base64.b64decode(value_z_b64)
    value_b64 = zlib.decompress(value_z)
    value_b = base64.b64decode(value_b64)
    value = value_b.decode()
    
    return value
