def warning(what: str)->None:
    print('[WARNING]', what)

def send(id: int, message: str, type:str='group')->None:
    print('[INFO]', 'send to {}, msg = "{}", type = "{}"'.format(id, message, type))
