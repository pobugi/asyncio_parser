import aiohttp
import asyncio
import json
from all_countries import Country
from time import time

async def get_country_borders(session, country_name):

    url = "https://restcountries.eu/rest/v2/name/{}".format(country_name)

    async with session.get(url) as resp:
        assert resp.status == 200
        # print("getting {}'s neighbouring countries......".format(country_name))
        response = await resp.text()
        neighbors = json.loads(response)[0]['borders']
        with open('neighbors.txt', 'a') as file:
            if neighbors:
                file.writelines(
                    country_name + "'s neighbors: " + ', '.join(str(n) for n in neighbors) + '\n'
                )
            else:
                file.writelines(country_name + "'s neighbors couldn't be found :(\n")
        return response


async def main():

    async with aiohttp.ClientSession() as session:
        tasks = []
        for country_name in all_countries:
            task = asyncio.create_task(get_country_borders(
                session, country_name
            ))
            tasks.append(task)
        await asyncio.wait(tasks)


if __name__ == '__main__':

    start = time()
    print('Sync parse started (making a list of countries...)')
    all_countries = Country().get_all_countries()
    print('Done, spent {} seconds\n'.format(round(time()-start, 2)))

    start = time()
    print('Async parse started (making a list of neghbouring countries...)')
    asyncio.run(main())
    print('Done, spent {} seconds'.format(round(time()-start, 2)))
    print("Check out 'neighbors.txt'")
