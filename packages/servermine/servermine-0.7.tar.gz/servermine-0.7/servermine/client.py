import datetime
import asyncio
import traceback
import time
import json
import uuid
import sys
import os
import importlib
import redis

import servermine.lib.redis_lib as redis_lib
import servermine.lib.acl as acl

project = "sm"
session_id = str(uuid.uuid4())
heartbeat_interval = 5
retry_delay = 5

imported_files = {}


def import_directories():
    files = os.listdir('./plugins')
    # print(files)
    sys.path.append('./plugins')
    for file in files:
        if file.endswith(".py"):
            try:
                file = file[:-3]
                imported_files.setdefault(file, importlib.import_module(file))
            except ImportError as err:
                print('Error:', err)
    # print(imported_files)


def set_project(p):
    global project
    project = p


def set_user(u):
    redis_lib.set_redis_user(u)


def set_password(p):
    redis_lib.set_redis_password(p)


def set_redis_url(url):
    redis_lib.set_redis_url(url)


def set_redis_api_key(key):
    acl.set_api_key(key)


def set_redis_api_secret(secret):
    acl.set_api_secret(secret)


async def start():
    # print("Start")
    import_directories()
    await asyncio.to_thread(queue())
    sub_server()


def import_directories():
    files = os.listdir('./plugins')
    # print(files)
    sys.path.append('./plugins')
    for file in files:
        if file.endswith(".py"):
            try:
                file = file[:-3]
                imported_files.setdefault(file, importlib.import_module(file))
                # users = importlib.import_module('plugins.users')
                # mtd = getattr(users, 'auth')
                # mtd()
                # users.auth()
            except ImportError as err:
                print('Error:', err)
    # print(imported_files)


def sub_server():
    # print("Sub Server")
    # r = await redis.from_url("redis://admin:V!6xU8Kf*sQqJS@redis-10264.c277.us-east-1-3.ec2.redns.redis-cloud.com:10264")
    session_data = {
        "type": "plugin",
        "sessionId": session_id,
        "project": project
    }

    # acl.create_acl("test2", "test123")

    redis_lib.get_redis_connection().hset(
        f'pp1:servers:{session_id}', mapping=session_data)
    redis_lib.get_redis_connection().expire(
        f'pp1:servers:{session_id}', heartbeat_interval)
    ev = {
        "channel": f'{project}:bl',
        "action": "server_up",
        "created": time.time_ns()
    }
    # get_redis_connection().hset(
    #     f'pp1:servers:{session_id}', mapping=session_data)
    # get_redis_connection().expire(
    #     f'pp1:servers:{session_id}', heartbeat_interval)
    # ev = {
    #     "channel": f'{project}:bl',
    #     "action": "server_up",
    #     "created": time.time_ns()
    # }
    redis_lib.get_redis_connection().publish(f'{project}:bl', json.dumps(ev))

    pubsub = redis_lib.get_redis_connection().pubsub()
    subscribe_channel(pubsub, f'{project}:br')

    # while True:
    #     try:
    #         # Listen for messages
    #         for message in pubsub.listen():
    #             if message['type'] == 'message':
    #                 print(f"Message received: {message['data']}")

    #     except Exception as e:
    #         time.sleep(5)
    #         pubsub = get_redis_connection().pubsub()
    #         subscribe_channel(pubsub, f'{project}:br')


def message_handler(message):
    if message['type'] == 'message':
        print(f"Message received: {message['data']}")


def subscribe_channel(pubsub, channel):
    # print("Subscribe")
    pubsub.subscribe(channel)
    pubsub.subscribe(**{channel: message_handler})
    pubsub.run_in_thread(sleep_time=0.001)


def queue():
    # print('Queue')
    # r = await redis.from_url("redis://admin:V!6xU8Kf*sQqJS@redis-10264.c277.us-east-1-3.ec2.redns.redis-cloud.com:10264")
    while True:
        # print(f'{project}:r')
        try:
            val = redis_lib.get_redis_connection().blpop(f'{project}:r', 5)
            if val:
                # print(val[1])
                job = json.loads(val[1])
                # print(job["data"])
                # print(job[""])
                if job["plugin"] in imported_files:
                    if hasattr(imported_files[job["plugin"]], job["action"]):
                        mtd = getattr(
                            imported_files[job["plugin"]], job["action"])
                        ret = mtd(job["data"])
                        job["data"] = ret
                        # print('job with data')
                        # print(job)
                        if "ws" in job:
                            redis_lib.get_redis_connection().rpush(
                                job["ws"], json.dumps(job))
                            redis_lib.get_redis_connection().expire(
                                job["ws"], 60)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            print("Redis connection lost. Reconnecting...")
            print(e)
            # traceback.print_exc()
            # Wait before attempting to reconnect
            time.sleep(retry_delay)

        except redis.exceptions.RedisError as e:
            # Catch other general Redis-related exceptions
            print("General Redis error")
            print(e)
            # traceback.print_exc()

        except Exception as e:
            print("Unexpected error on brpop queue")
            print(e)
            # traceback.print_exc()


if __name__ == '__main__':
    print('start')
    # redis.set_user("Teste")
#     try:
#         # loop = asyncio.get_event_loop()
#         # loop.run_until_complete(start())
#         asyncio.run(start())
#     except Exception as error:
#         print(error)
#         traceback.print_exc()
#     # asyncio.run(start())
