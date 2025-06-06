import configparser

def read_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    
    youtube_config = {
        'api_key': config.get('YouTube', 'api_key'),
    }

    return youtube_config