import os
import yaml 
import datetime 

def get_config(env, config_resource):
    '''
        Load config options for the given environment 
        * ``env`` - yaml key ( i.e. parent field -->  e.g.  dev_lite )
        * ``config_resource`` - file object referencing config.yaml file 
    '''

    # read yaml file
    config_dict = yaml.load(config_resource, Loader=yaml.Loader)
    print(config_dict)
    # parse yam file using key or parent field env
    try:
        config_dict = config_dict[env]
    except KeyError:
        raise KeyError("Invalid ENV value '{}' should be in {}, set using FLASK_ENV=value".format(env, list(config_dict())))
    
    # Load any FLASK_ environment variables 
    for key, value in os.environ.items():
        if key.startswith('FLASK_'):
            config_dict[key[6:]] = value 
        
    # Load any env: values from environment 
    for key, value in config_dict.items():
        if isinstance(value, str) and value.startswith('env:'):
            config_dict[key] = os.environ[value[4:]]

    # Put the values into application config
    return config_dict 

def date_to_ordinal(dt):
    '''
        Given Datetime or None value ``dt``, return either None or the
        ordinal value for the DateTime. Used for preparing to serialize to JSON
    '''

    if dt is None:
        return None 
    elif isinstance(dt, datetime.datetime):
        return dt.toordinal() # returns proleptic Gregorian ordinal of the date 
    else:
        return 'unknown'