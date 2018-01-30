def input (job):
    '''
    create key, if it doesn't exist
    '''
    args = job.model.args
    if 'key.path' in job.model.args and job.model.args['key.path'] is not None and job.model.args['key.path'] != '':
        path = job.model.args['key.path']
        if not j.sal.fs.exists(path, followlinks=True):
            raise j.exceptions.Input(message="Cannot find ssh key:%s for service:%s" %
                                     (path, job.service), level=1, source="", tags="", msgpub="")
        args['key.path'] = j.sal.fs.joinPaths(job.service.path, "id_rsa")
        j.sal.fs.createDir(job.service.path)
        j.sal.fs.copyFile(path, args['key.path'])
        j.sal.fs.copyFile(path + '.pub', args['key.path'] + '.pub')
        args["key.priv"] = j.sal.fs.fileGetContents(path)
        args["key.pub"] = j.sal.fs.fileGetContents(path + '.pub')
    if 'key.name' in job.model.args and bool(job.model.args.get('key.name')):
        path = j.clients.ssh.SSHKeyGetPathFromAgent(job.model.args['key.name'])
        if not path or not j.sal.fs.exists(path, followlinks=True):
            raise j.exceptions.Input(message="Cannot find ssh key:%s for service:%s" %
                                     (path, job.service), level=1, source="", tags="", msgpub="")
        args["key.priv"] = j.sal.fs.fileGetContents(path)
        args["key.pub"] = j.sal.fs.fileGetContents(path + '.pub')
        args["key.name"] = job.model.args["key.name"]
        args["key.path"] = j.sal.fs.joinPaths(job.service.path, job.model.args['key.name'])
        j.sal.fs.createDir(job.service.path)
        j.sal.fs.copyFile(path, j.sal.fs.joinPaths(job.service.path, args["key.path"]))
        j.sal.fs.copyFile(path + '.pub', j.sal.fs.joinPaths(job.service.path, '%s.%s' % (args["key.path"], 'pub')))
    if 'key.priv' not in args or args['key.priv'].strip() == "":
        print("lets generate private key")
        args['key.path'] = j.sal.fs.joinPaths(job.service.path, "id_rsa")
        j.sal.fs.createDir(job.service.path)
        j.sal.fs.remove(args['key.path'])
        cmd = "ssh-keygen -q -t rsa -f %s -N ''" % (args['key.path'])
        rc, out, err = j.sal.process.execute(cmd, die=True, outputStderr=False)
        args["key.priv"] = j.sal.fs.fileGetContents(args['key.path'])
        args["key.pub"] = j.sal.fs.fileGetContents(args['key.path'] + '.pub')
    j.sal.fs.chmod(args['key.path'], 0o600)
    j.sal.fs.chmod(args['key.path']+ '.pub', 0o600)
    return args
    

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
    

