def input (job):
    return None
    

def init (job):
    pass
    

def install (job):
    pass
    

def stop (job):
    pass
    

def start (job):
    pass
    

def monitor (job):
    pass
    

def halt (job):
    pass
    

def check_up (job):
    pass
    

def check_down (job):
    pass
    

def check_requirements (job):
    pass
    

def cleanup (job):
    pass
    

def data_export (job):
    pass
    

def data_import (job):
    pass
    

def uninstall (job):
    pass
    

def removedata (job):
    pass
    

def consume (job):
    pass
    

def action_pre_ (job):
    pass
    

def action_post_ (job):
    pass
    

def init_actions_ (service, args):
    '''
    this needs to returns an array of actions representing the depencies between actions.
Looks at ACTION_DEPS in this module for an example of what is expected

    '''
    
    # some default logic for simple actions
    
    action_required = args.get('action_required')
    
    if action_required in ['stop', 'uninstall']:
        for action_name, action_model in service.model.actions.items():
            if action_name in ['stop', 'uninstall']:
                continue
            if action_model.state == 'scheduled':
                action_model.state = 'new'
    
    if action_required in ['install']:
        for action_name, action_model in service.model.actions.items():
            if action_name in ['uninstall', 'stop'] and action_model.state == 'scheduled':
                action_model.state = 'new'
    
    
    if action_required == 'stop':
        if service.model.actionsState['start'] == 'sheduled':
            service.model.actionsState['start'] = 'new'
    
    if action_required == 'start':
        if service.model.actionsState['stop'] == 'sheduled':
            service.model.actionsState['stop'] = 'new'
    
    service.save()
    
    return {
        'init': [],
        'install': ['init'],
        'start': ['install'],
        'monitor': ['start'],
        'stop': [],
        'delete': ['uninstall'],
        'uninstall': ['stop'],
    }
    
    

def delete (job):
    job.service.delete()
    

