import asyncio

async def buaklek(a,b):
    c = a+b
    print('Function Started')
    return c

async def main():
    coru = buaklek(13,10)
    task = asyncio.create_task(coru)
    phonbuak = await task
    print('sum is %s'%phonbuak)

maincoru = main()
asyncio.run(maincoru)