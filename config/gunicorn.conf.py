
def when_ready(server):
    '''
        creates an empty file in the tmp directory 
    '''
    open('/tmp/app-initialized', 'w').close() 

bind = 'unix:///tmp/nginx.socket'