import redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
try:
    r.ping()
    print('Успешно!')
except redis.ConnectionError:
    print('Ошибка!')

client = r

r.set('user:name', 'Иван')
name = r.get('user:name').encode('utf-8')

r.setex('session:123', 3600, 'active')

r.set('counter', 0)
r.incr('counter')
r.incrby('counter', 5)
r.decr('counter')

r.lpush('tasks', 'task1', 'task2')
r.rpush('tasks', 'task1', 'task2')

tasks = r.lrange('tasks', 0, -1)
first_task = r.lpop('tasks')
last_task = r.rpop('tasks')

length = r.llen('tasks')

r.sadd('tags', 'python', 'redis', 'database')
r.sadd('languages', 'python', 'java', 'javascript')

is_member = r.sismember('tags', 'python')

all_tags = r.smembers('tags')

instersection = r.sinter('tags', 'languages')
union = r.sunion('tags', 'languages')
difference = r.sdiff('tags', 'languages')

r.hset('user:1000', mapping={
    'name': 'Иван',
    'age': '30',
    'city': 'Москва'
})

name = r.hget('user:1000', 'name')
all_data = r.hgetall('user:1000')

exists = r.hexists('user:1000', 'email')

keys = r.hkeys('user:1000')
values = r.hvals('user:1000')

r.zadd('leaderboard', {
    'p1': 100,
    'p2': 200,
    'p3': 300,
})

top_players = r.zrange('leaderboard', 0, 2, withscores=True)

players_by_score = r.zrangebyscore('leaderboard', 100, 200)

rank = r.zrank('leaderboard', 'p1')