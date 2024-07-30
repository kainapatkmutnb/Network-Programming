import asyncio, time

async def ioioio(wela, chue_khanom):
    print(' Started baking %s, %.5f seconds elapsed'%(chue_khanom,time.time()-t0))
    await asyncio.sleep(wela)
    print('Finished baking %s, %.5f seconds elapsed'%(chue_khanom,time.time()-t0))
    return '*'+chue_khanom+'finished baking*'

async def main():
    cococoru = [ioioio(2, ' tofu' ) , ioioio (3.5, ' cake' ) , ioioio(3, 'sausage ' ) , ioioio(1, 'croissant' ) ]
    phonlap = await asyncio.gather(*cococoru)
    print(phonlap)

t0 = time.time()
asyncio. run(main ())