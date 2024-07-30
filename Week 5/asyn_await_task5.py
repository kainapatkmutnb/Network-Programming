import asyncio,time

async def ioioio(wela,chue_ngan):
    print('Start%s Time has passed %.5f Second'%(chue_ngan,time.time()-t0))
    await asyncio.sleep(wela)
    print('%sDone Time has passed %.5f Second'%(chue_ngan,time.time()-t0))
    return

async def main():
    print('Started function')
    phara1 = asyncio.create_task(ioioio(1.5,'Downloading Music'))
    phara2 = asyncio.create_task(ioioio(2.5,'Downloading Anime'))
    phara3 = asyncio.create_task(ioioio(0.5,'Downloading Movie'))
    print('Created Mission')
    await phara2
    print('Function Complete')

t0 = time.time()
asyncio.run(main())