import asyncio

async def buaklek(a,b):
    return a+b

async def main():
    phonbuak = await buaklek(13,10)
    print('sum is %s'%phonbuak)

asyncio.run(main())