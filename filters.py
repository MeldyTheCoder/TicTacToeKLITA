import json

def isPublic():
    return lambda message: message.chat.type != 'private'

def query(query_string: str):
    return lambda query: json.loads(query.data)['action'] == query_string

def isPublicQuery():
    return lambda query: query.message.chat.type != 'private'

def isPrivate():
    return lambda query: query.message.chat.type == 'private'