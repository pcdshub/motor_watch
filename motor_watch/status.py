def process(status):
    dict = {}
    dict['name'] = status.pos.name
    dict['target'] = status.target
    return dict
