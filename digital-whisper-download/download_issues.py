#! /usr/bin/env python3

import os
import asyncio
import re
import aiohttp
import aiofiles
import click

SITE = "https://www.digitalwhisper.co.il"
LOCATION_IN_SITE = "files/Zines/{hexa}/DigitalWhisper{decimal}.pdf"
URL = "/".join([SITE, LOCATION_IN_SITE])
DEFAULT_ISSUE_FORMAT = "DigitalWhisper{}.pdf"
FIND_NUMBER = "[1-9][0-9]*"
OK = 200
# -rwxrw-rw-
FILE_PERMISSIONS = 0o766


def convert_to_hexadecimal(number):
    return "0x" + "{0:X}".format(int(number)).zfill(2)


def generate_urls(issues):
    for issue in issues:
        yield URL.format(hexa=convert_to_hexadecimal(issue),
                         decimal=issue)


async def issue_downloader(path, url, issue_format):
    print("Downloading issue from url: {url}".format(url=url))
    issuename = re.search(issue_format.format(FIND_NUMBER), url).group()
    filename = os.path.join(path, issuename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == OK:
                async with aiofiles.open(filename, mode="wb") as f:
                    await f.write(await response.read())
                    os.chmod(filename, FILE_PERMISSIONS)
    print("Done downloading issue from url: {url}".format(url=url))


async def issues_downloader(path, issues, issue_format):
    tasks = []
    for url in generate_urls(issues):
        tasks.append(asyncio.ensure_future(
                        issue_downloader(
                            path, url, issue_format)))
    asyncio.gather(*tasks)


@click.command()
@click.option("--issue-number", type=int,
              default=None, help="download a specific issue")
@click.option("--max-issue", type=int,
              help="the latast issue to download")
@click.option("--min-issue", type=int, default=0,
              help="the first issue to download")
@click.option("--path", default=os.getcwd(),
              help="where to store the downloaded issues")
def download_issues(issue_number, max_issue, min_issue, path,
                    issue_format=DEFAULT_ISSUE_FORMAT):
    if issue_number is not None:
        max_issue = issue_number
        min_issue = issue_number

    issues = list(range(min_issue, max_issue + 1))
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            issues_downloader(path=path, issues=issues,
                              issue_format=issue_format))
        for t in asyncio.Task.all_tasks():
            if not t.done() or t.cancelled():
                loop.run_until_complete(t)
    finally:
        loop.close()


if __name__ == '__main__':
    download_issues()
