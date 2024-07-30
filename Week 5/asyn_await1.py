import asyncio

async def main():
    print('aektawan')
    await foo('text')
    print('finished')

async def foo(text):
    print(text)
    await asyncio.sleep(2)

asyncio.run(main())