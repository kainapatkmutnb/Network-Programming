import asyncio

async def hanlek(a,b):
    print('%s / %s' % (a,b))
    return a / b

loop = asyncio.get_event_loop()
phonhan = loop. run_until_complete(hanlek(7,6))
print('Result: %.3f'%phonhan)