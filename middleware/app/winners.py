import redis

def store(key, value):
  r = redis.Redis('localhost')
  retv = r.set(key, value)
  return retv
