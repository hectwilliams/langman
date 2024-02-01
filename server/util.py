import os
import yaml 
import datetime 

def get_config(env, config_resource):
    '''
        Load config options for the given environment:
            * ``env`` - yaml key ( i.e. parent field -->  e.g.  dev_lite )
            * ``config_resource`` - file object referencing config.yaml file 
    '''
    # read yaml file
    config_dict_yaml = yaml.load(config_resource, Loader=yaml.Loader)
    
    # parse yaml file using key or parent field env
    try:
        config_dict = config_dict_yaml[env]
    except KeyError:
        raise KeyError("Invalid ENV value '{}' should be in {}, set using FLASK_ENV=value".format(env, list(config_dict())))
    
    # Load DB init key/value pair 
    config_dict['PREVIOUS_DB_INIT'] = config_dict_yaml.get('config').get('PREVIOUS_DB_INIT')

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

def init_usage_table():

    resource = open('server/config.yaml')       
    config_dict_yaml = yaml.load(resource,  Loader=yaml.Loader)
    init_db_bool = False 

    with open('server/config.yaml', 'w+') as file:

        old_yaml_update = config_dict_yaml['config']['PREVIOUS_DB_INIT'] 

        if old_yaml_update == 0:
            old_yaml_update =  datetime.datetime.now().strftime("%Y%m%d%H%M%S") 
        
        old_yaml_update = datetime.datetime.strptime(old_yaml_update, '%Y%m%d%H%M%S') 

        delta = datetime.datetime.now() - old_yaml_update
        if delta.total_seconds() > 0 :
            # re-update yaml file
            config_dict_yaml['config']['PREVIOUS_DB_INIT'] = (datetime.datetime.now() + datetime.timedelta(days=30)) .strftime("%Y%m%d%H%M%S") 
            init_db_bool = True 
        
        yaml.dump(config_dict_yaml, file)

    return init_db_bool  