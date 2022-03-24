"""Redis utility function for setting and retrieving data"""


import msgpack

def set_dict_redis(redis , key, dictionary):
    """
    Sets the dictonary values in redis
    Input: redis object, image name (key), updated data(dictonary)
    Output: None
    """
    redis.set(key, msgpack.packb(dictionary))

def get_dict_redis(redis, key):
    """
    Gets the dictonary values in redis
    Input: redis object, image name (key)
    """
    value = redis.get(key)
    return msgpack.unpackb(value)