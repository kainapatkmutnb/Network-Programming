import asyncio

async def main():
    print('aektawan')
    task = asyncio.create_task(foo('text'))
    await task
    print('finished')

async def foo(text):
    print(text)
    await asyncio.sleep(3)

asyncio.run(main())