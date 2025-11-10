#!/usr/bin/python3
#
""" Script to scan a built website & report on links that are broken. """

import argparse
import asyncio
import concurrent
import io
import json
import os
import socket
import sys
import traceback
from os.path import join
from urllib.parse import unquote, urlparse

import aiohttp
import requests
from bs4 import BeautifulSoup

# The link checking process depends on whether it is a relative
# or absolute link. If it is a relative link, a file is looked for
# that matches the relative path.
#
# If it is an absolute link, the pair of filename and link are stored,
# along with a list of unique links to be checked. At the end of the
# scan, all of the unique links are checked in an async process and
# the results stored. Those results are then used to update the list
# of filename/link pairs.


CHROME = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/41.0.2228.0 Safari/537.36'
}

# This is a list of files that should always be removed from the
# ALL_FILES list before printing the list of unreferenced files.
# It is, unfortunately, a bit of a hacky list since language
# variants cause their own versions of certain files to be added
# which means that this list must include all potential languages.
PROTECTED_FILES = [
    "./robots.txt",
    "./favicon.ico",
    "./admin/index.html",
    "./admin/config.yml",
    "./404.html",
    "./ch/404.html",
    "./feed.xml",
    "./ch/feed.xml"
]

# Globals
ALL_FILES = []
FAILED_DIRS = []
FAILED_LINKS = []
FILE_LINK_PAIRS = []
UNIQUE_LINKS = []
STATUS_COUNT = 1
HTML_CACHE_RESULTS = {}
DNS_SKIP = []
VERBOSE = 0
OUTPUT_FILE = None

def reference_file(filename):
    """ If filename is in the list, remove it """
    if filename in ALL_FILES:
        ALL_FILES.remove(filename)
        return True
    return False


def drop_dot(string_to_check):
    """ If the string starts with a full-stop, drop it. """
    if string_to_check != "" and string_to_check[0] == '.':
        return string_to_check[1:]
    return string_to_check


def get_all_html_files(path):
    """
    Return a list of all of the HTML files in the path and
    below.
    """
    result = []
    for root, dirs, files in os.walk(path):
        process_html_files(result, files, root)
        process_html_dirs(dirs, root)
    return result


def process_html_files(result, files, root):
    """
    For a given list of files, update the list with
    any that are HTML files.
    """
    global ALL_FILES # pylint: disable=global-statement
    for name in files:
        file_path = os.path.join(root, name)
        if name.endswith((".html", ".htm")) and \
            file_path not in result:
                result.append(file_path)
        # We record ALL of the files that have been found
        # so that we can then remove them when they are
        # referenced and report any files not touched.
        if file_path not in ALL_FILES:
            ALL_FILES.append(file_path)


def process_html_dirs(dirs, root):
    """
    For a given list of directories, check that none of the directories
    has a full-stop in the name. Note that we do not need to recurse
    through the directories because os.walk does that already for all of
    the files.
    """
    global FAILED_DIRS # pylint: disable=global-statement
    for directory in dirs:
        if "." in directory:
            path = join(root, directory)
            if path not in FAILED_DIRS:
                FAILED_DIRS.append(path)


def validate_file_link(filename, text):
    """ Check that the specified file-based object exists. """
    # If there is an anchor (#) in the text, we need to look at what
    # comes before it.
    text = text.split("#")[0]
    # If there is a query (?) in the text, we need to look at what
    # comes before it.
    text = text.split("?")[0]
    #
    # After that, we may actually end up with an empty string because
    # it could be something like "?foo" or "#foo"
    if text == "":
        return None
    # If "text" starts with "/" then we need to be looking at the
    # path relative to where we started scanning.
    #
    # Otherwise, it will be relative to where the current file is
    # located.
    if text[0] == "/":
        head = "."
    else:
        # Text will be pointing at a directory or file, relative to
        # where the parent file is living.
        # head gets us the directory where the parent file lives.
        head, _ = os.path.split(filename)
    if head[-1] != '/' and text[0] != '/':
        combined_path = "%s/%s" % (head, text)
    else:
        combined_path = "%s%s" % (head, text)
    # If the path contains a double-slash, that works on the OS but not in the
    # browser so we need to explicitly check for it.
    if "//" in combined_path:
        return combined_path
    # If we're looking at a directory, make sure there is an index file in it.
    if combined_path[-1] == '/':
        combined_path += "index.html"
    if VERBOSE >= 2:
        print(("Validating file: constituent parts are '%s' and '%s',"
               " combined path is '%s'") % (head, text, combined_path))
    # Unquote the string in case there are spaces or other odd chars ...
    unescaped_path = unquote(combined_path)
    if unescaped_path != combined_path:
        combined_path = unescaped_path
        if VERBOSE >= 2:
            print("Unescaped file: %s" % unescaped_path)
    # needs to be a file or directory ... but if it is a directory, that means
    # the path didn't end with a "/" (because we would have added index.html)
    # so we now add that back to the path so that the file referencing process
    # correctly marks the file as referenced.
    if os.path.isfile(combined_path):
        reference_file(combined_path)
        return None
    if os.path.isdir(combined_path):
        # Is there a "index.html" inside that folder?
        temp_path = f"{combined_path}/index.html"
        if os.path.isfile(temp_path):
            reference_file(temp_path)
            return None
    return combined_path


def matched_skip(text, skip_list):
    """ Check if text is in the skip list. """
    if skip_list is not None:
        for skip in skip_list:
            if text.startswith(skip):
                return True
    return False


def validate_link(filename, text, check_unrefs_only=False):
    """ Main link validation processor. """
    global FILE_LINK_PAIRS # pylint: disable=global-statement
    global UNIQUE_LINKS # pylint: disable=global-statement
    # Clean up the text first ...
    if text is not None:
        text = text.strip()
    if text is None or text == "" or text[0] == "#":
        # or matched_redirect(text):
        return None
    # Some links don't have the transport on them to ensure that they work
    # whether the user is coming via http or https, so add it if it is
    # missing.
    if len(text) > 2 and text[:2] == "//":
        text = "https:" + text
    # Check the URL to see if it is a web link - that is all we check.
    obj = urlparse(text)
    if not args.noexternal and (obj.scheme == "http" or obj.scheme == "https"):
        # If we are checking unreferenced files, don't worry about
        # external links.
        if check_unrefs_only:
            return None
        # We use "file_link_pairs" to track which files reference which
        # URLs - we only check URLs *once* but then flag up all
        # refernces to the link.
        if [filename, text] not in FILE_LINK_PAIRS:
            FILE_LINK_PAIRS.append([filename, text])
        # ... only check the links once!
        if text not in UNIQUE_LINKS:
            UNIQUE_LINKS.append(text)
        return None  # Postpone the decision for now ...
    if not args.nointernal and obj.scheme == "":
        return validate_file_link(filename, text)
    # If skipping stuff, return the answer of no problems ...
    return None


def output_status(code, value):
    """ Output the status in blocks of 100 """
    global STATUS_COUNT # pylint: disable=global-statement

    if STATUS_COUNT % 100 == 0:
        end = "\n"
    else:
        end = ""
    print(code, end=end, flush=True)
    STATUS_COUNT += 1
    return value


async def async_url_validation(session, url):
    """ Validate the URL. """
    async with session.head(
            url,
            allow_redirects=True,
            headers=CHROME) as response:
        if response.status == 404 or response.status == 405:
            # Some sites return 404/405 for HEAD requests, so we need to
            # double-check with a full request.
            async with session.get(
                    url,
                    allow_redirects=True,
                    headers=CHROME) as response:
                if response.status != 404 and response.status != 405:
                    return output_status('.', 0)
                return output_status('X', response.status)
        else:
            if (response.status < 400 or
                    response.status > 499):
                return output_status('.', 0)
            if VERBOSE >= 3:
                print(response.status, response.url)
            # We only really care about full-on failures, i.e. 404.
            # Other status codes can be returned just because we aren't
            # using a browser, even if we do provide the agent string
            # for Chrome.
            return output_status('_', 0)


async def async_check_link(session, url):
    """ Check the external link. """
    # Check that the host resolves, but only if it isn't in the DNS skip list
    parts = urlparse(url)
    if parts.netloc not in DNS_SKIP:
        try:
            _ = socket.gethostbyname(parts.netloc)
        except socket.gaierror as err:
            return output_status('D', 1)
    # Now try to validate the URL
    try:
        return await async_url_validation(session, url)
    # (Non-)Fatal errors
    except socket.gaierror as err:
        print("Error while checking %s: %s" % (url, err))
        return output_status('a', -2)
    # Non-fatal errors, but indicate which error we are getting
    except aiohttp.client_exceptions.ClientConnectorError:
        return output_status('b', -3)
    except aiohttp.client_exceptions.ServerTimeoutError:
        return output_status('c', -4)
    except concurrent.futures._base.CancelledError: # pylint: disable=protected-access
        return output_status('d', -5)
    except concurrent.futures._base.TimeoutError: # pylint: disable=protected-access
        return output_status('e', -6)
    except aiohttp.client_exceptions.ClientOSError:
        return output_status('f', -7)
    except aiohttp.client_exceptions.ServerDisconnectedError:
        return output_status('g', -8)
    except aiohttp.client_exceptions.ClientResponseError:
        return output_status('h', -9)
    except asyncio.TimeoutError:
        return output_status('i', -10)


async def async_check_web(session, links):
    """ Check all external links. """
    results = await asyncio.gather(
        *[async_check_link(session, url) for url in links]
    )
    # That gets us a collection of the responses, matching up to each of
    # the tasks, so loop through the links again and the index counter
    # will point to the corresponding result.
    i = 0
    for link in links:
        if link not in HTML_CACHE_RESULTS:
            if results[i] == 0:
                HTML_CACHE_RESULTS[link] = None
            elif results[i] > 0:
                HTML_CACHE_RESULTS[link] = "%s [%d]" % (link, results[i])
        i += 1


async def check_unique_links():
    """
    Perform an async check of all of the web links we've collected then
    build up a list of the affected files for the faulty links.
    """
    global STATUS_COUNT # pylint: disable=global-statement
    STATUS_COUNT = 1

    web_failed_links = []
    print("Checking %s web links ..." % len(UNIQUE_LINKS))
    # Force IPv4 only to avoid
    # https://stackoverflow.com/questions/40347726/python-3-5-asyincio-and-aiohttp-errno-101-network-is-unreachable
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        ssl=False,
        limit=500
    )
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(connector=conn,
                                     timeout=timeout) as session:
        await async_check_web(session, UNIQUE_LINKS)
    for pair in FILE_LINK_PAIRS:
        # p[0] is the file path and p[1] is the URL.
        if (pair[1] in HTML_CACHE_RESULTS and
                HTML_CACHE_RESULTS[pair[1]] is not None):
            error = [pair[0], HTML_CACHE_RESULTS[pair[1]]]
            if error not in web_failed_links:
                web_failed_links.append(error)
    return web_failed_links


def check_file(filename, skip_list):
    """
    For the specified file, read it in and then check all of the links
    in it.
    """
    if matched_skip(filename, skip_list):
        return []

    file_failed_links = []
    try:
        with open(filename, "r") as myfile:
            data = myfile.read()
        soup = BeautifulSoup(data, 'html.parser')
        check_links(filename, soup, file_failed_links)
        check_linked_images(filename, soup, file_failed_links)
        check_remaining_references(filename, soup)
    except Exception as exception: # pylint: disable=broad-except
        print(f"FAILED TO READ '{filename}'")
        traceback.print_exc()
    return file_failed_links


def check_remaining_references(filename, soup):
    """
    For all non-file/image links, remove the referenced files from
    the global list.
    """
    links = soup.find_all('link')
    for link in links:
        file = link.get('href')
        validate_link(filename, file, True)
        validate_link(filename, f"{file}.gz", True)
    # A trickier bit to check is the "picture" attribute which uses
    # "source" and then a "data-srcset" tag. The "data-srcset" tag
    # lists multiple images and needs to be parsed/split up into
    # individual filenames for removal from the global list.
    links = soup.find_all('source')
    for link in links:
        process_sources(link.get('data-srcset'))
    # Script loading
    links = soup.find_all('script')
    for link in links:
        validate_link(filename, link.get('src'), True)
    # Forms
    links = soup.find_all('form')
    for link in links:
        validate_link(filename, link.get('action'), True)
    

def process_sources(file_refs):
    """ Check the source set off against the list of files """
    if file_refs is None:
        return

    # A sample data-srcset:
    # data-srcset="/../generated/assets/images/content/code_banner-576-65b154.webp 576w,
    #  /../generated/assets/images/content/code_banner-768-65b154.webp 768w,
    #  /../generated/assets/images/content/code_banner-992-65b154.webp 992w,
    #  /../generated/assets/images/content/code_banner-1200-65b154.webp 1200w,
    #  /../generated/assets/images/content/code_banner-1920-65b154.webp 1920w"
    #
    # So, start by splitting on the comma:
    parts = file_refs.split(",")
    # then iterate, splitting on the space:
    removed_from_list = False
    for part in parts:
        file = part.strip().split(" ")[0]
        if file[:4] == "/../":
            # Trim "/." off the front so that we're left with "./" which will
            # then match against the filenames
            file = file[2:]
            if reference_file(file):
                removed_from_list = True
        elif file[0] == "/":
            file = "." + file
            if reference_file(file):
                removed_from_list = True
        else:
            print(f"Unable to parse '{file}'")
            print(f"Original was '{part}'")
            sys.exit(1)
    # Finally, if we removed the generated assets from the list, try(!) to
    # extract the filename of the original source image so that we can mark
    # that as referenced.
    if removed_from_list:
        orig = parts[0].strip().split(" ")[0]
        # Strip off "/../generated" and then add a leading full-stop to
        # match the full path to the original image.
        orig = "." + orig[13:]
        # Now split the string at the first hyphen which *should* split it at
        # the size indicator.
        orig_parts = orig.split("-")
        to_match = orig_parts[0]
        matched = None
        # and try to find the original
        for unref in ALL_FILES:
            if unref[:len(to_match)] == to_match:
                matched = unref
                break
        if matched is not None:
            reference_file(matched)


def check_links(filename, soup, file_failed_links):
    """ Check all links found in the file. """
    a_links = soup.find_all('a')
    # Linaro specific ... find any "edit on GitHub" links so that
    # they can be EXCLUDED from the list of links to check. The reason
    # why is because if this is a new page (i.e. in a Pull Request),
    # the file won't exist in the repository yet and so the link to
    # the page would fail.
    gh_links = soup.find_all('a', id="edit_on_github")
    for link in gh_links:
        a_links.remove(link)
    for link in a_links:
        result = validate_link(filename, link.get('href'))
        if result is not None:
            error = [filename, result]
            if error not in file_failed_links:
                file_failed_links.append(error)


def check_linked_images(filename, soup, file_failed_links):
    """ Check that all of the image links are valid. """
    img_links = soup.find_all('img')
    for link in img_links:
        result = validate_link(filename, link.get('src'))
        if result is not None:
            error = [filename, result]
            if error not in file_failed_links:
                file_failed_links.append(error)


def failures_to_dict(list_of_failures):
    """ Convert the list into a dictionary. """
    failure_dict = {}
    for failure in list_of_failures:
        file = drop_dot(failure[0])
        url = drop_dot(failure[1])
        if file in failure_dict:
            failure_dict[file].append(url)
        else:
            failure_dict[file] = [url]
    return failure_dict


def scan_directory(path, skip_list, create_gh_issue, assign_gh_issue, gh_token):
    """ Scan the specified directory, ignoring anything that matches skip_list. """
    global FAILED_LINKS # pylint: disable=global-statement
    global FILE_LINK_PAIRS # pylint: disable=global-statement
    global UNIQUE_LINKS # pylint: disable=global-statement
    FAILED_LINKS = []
    FILE_LINK_PAIRS = []
    UNIQUE_LINKS = []

    soft_failure = False

    html_files = get_all_html_files(path)
    total = len(html_files)
    if args.file is not None:
        total = len(args.file)
    scan_html_files(html_files, skip_list, total)
    if len(UNIQUE_LINKS) == 0:
        print("No web links to check.")
    else:
        soft_failure = scan_web_links()
    if FAILED_LINKS != [] or FAILED_DIRS != []:
        if create_gh_issue is None:
            output_failed_links()
        else:
            github_create_issue(create_gh_issue, assign_gh_issue, gh_token)
    if soft_failure:
        print("\nLinks have been checked; warnings reported.")
    else:
        print("\nLinks have been successfully checked.")


def scan_html_files(html_files, skip_list, total):
    """ Scan each of the specified HTML files. """
    global FAILED_LINKS # pylint: disable=global-statement
    count = 1
    for this_file in html_files:
        if args.file is None or this_file in args.file:
            print("(%s/%s) Checking '%s'" % (count, total, this_file))
            count += 1
            results = check_file(this_file, skip_list)
            for res in results:
                if res not in FAILED_LINKS:
                    FAILED_LINKS.append(res)


def scan_web_links():
    """ Scan all of the discovered external links. """
    global FAILED_LINKS # pylint: disable=global-statement
    soft_failure = False
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    cul_result = loop.run_until_complete(check_unique_links())
    loop.close()
    # If we are NOT reporting broken external links as an error,
    # report them as warnings if there are any.
    if args.no_external_errors:
        if cul_result != []:
            print("\n\nWARNING! %s failed external links have been "
                    "found:\n" % len(cul_result))
            report_failed_links(cul_result, sys.stdout)
            soft_failure = True
    else:
        # Can do a simple append here because these are all web failures
        # and so don't need to check if the failure already exists in the
        # list.
        FAILED_LINKS += cul_result
    return soft_failure


def github_create_issue(issue_url, assignees, token):
    """ Create a GitHub issue to report the failed links. """
    subject = ""
    fsock = io.StringIO()
    if FAILED_DIRS != []:
        subject = "%s directories with full-stops in name (invalid)" % len(FAILED_DIRS)
        print("```", file=fsock)
        report_failed_dirs(FAILED_DIRS, fsock)
        print("```", file=fsock)
    if FAILED_LINKS != []:
        if subject != "":
            subject += ", "
        subject += "%s failed links" % len(FAILED_LINKS)
        print("%s failed links have been found:" % len(FAILED_LINKS), file=fsock)
        print("```", file=fsock)
        report_failed_links(FAILED_LINKS, fsock)
        print("```", file=fsock)

    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": "token %s" % token
    }
    payload = {
        "title": subject,
        "body": fsock.getvalue(),
        "assignees": json.loads(assignees)
    }
    result = requests.post(
        url=issue_url,
        json=payload,
        headers=headers)
    if result.status_code == 201:
        print("Failed links issue created at %s" % result.json()["html_url"])

def output_failed_links():
    """ Output a list of failed links to stdout or a file. """
    output_to = sys.stdout
    if OUTPUT_FILE is not None:
        output_to = open(OUTPUT_FILE, 'w')
    else:
        print("")
    if FAILED_DIRS != []:
        print(
            "%s directories found with full-stops in name (invalid):\n" % len(FAILED_DIRS),
            file=output_to)
        report_failed_dirs(FAILED_DIRS, output_to)
    if FAILED_LINKS != []:
        print("%s failed links found:\n" % len(FAILED_LINKS), file=output_to)
        report_failed_links(FAILED_LINKS, output_to)
    if OUTPUT_FILE is not None:
        output_to.close()
    # sys.exit(1)


def report_failed_dirs(dir_list, output_to):
    """ Report any directories with full-stops in their names. """
    for directory in dir_list:
        print(directory, file=output_to)


def report_failed_links(link_list, output_to):
    """ Report all of the failed links for a given file. """
    failure_dict = failures_to_dict(link_list)
    for file in sorted(failure_dict):
        print("%s:" % file, file=output_to)
        for ref in failure_dict[file]:
            print("   %s" % ref, file=output_to)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scan for broken links")
    parser.add_argument('-d', '--directory', nargs='?', default=None,
                        help='specifies the directory to scan')
    # parser.add_argument('-r', '--redirects', nargs='?', default=None,
    #                     help='specifies optional CSV file of URL redirects')
    parser.add_argument('--skip-dns-check', nargs='?', default=None,
                        help='specifies text file of FQDNs to skip the DNS '
                        'check on')
    parser.add_argument('--referenced-file-list', nargs='?', default=None,
                        help='specified text file of ')
    parser.add_argument('-s', '--skip-path', action='append',
                        help='specifies a path to skip when checking URLs')
    parser.add_argument('-v', '--verbose', action='count')
    parser.add_argument('-f', '--file', action='append',
                        help=('specifies a file to check;'
                              ' all non-specified files are ignored'))
    parser.add_argument('--nointernal', action='store_true',
                        help='skips checking of internal references')
    parser.add_argument('--noexternal', action='store_true',
                        help='skips checking of external references')
    parser.add_argument('-o', '--output', nargs='?', default=None,
                        help='specifies output file for error results')
    parser.add_argument('--no-external-errors', action='store_true',
                        help='ignores errors caused by external broken links')
    parser.add_argument('--create-github-issue', action='store',
                        help='creates issue on specified repo url')
    parser.add_argument('--assign-github-issue', action='store',
                        help='assigns the created issue to the array of names')
    parser.add_argument('--github-access-token', action='store')
    args = parser.parse_args()

    print("Linaro Link Checker (2023-04-11)")

    if args.verbose is not None:
        VERBOSE = args.verbose
    if args.skip_dns_check is not None:
        print("Loading FQDN skip list from %s" % args.skip_dns_check)
        try:
            DNS_SKIP = list(open(args.skip_dns_check))
        except Exception as exception: # pylint: disable=broad-except
            print("Couldn't load FQDN skip list")
    if args.output is not None:
        OUTPUT_FILE = args.output
    if args.directory is not None:
        print("Scanning '%s'" % args.directory)
        os.chdir(args.directory)
    if args.nointernal:
        print("Skipping internal link checking")
    if args.noexternal:
        print("Skipping external link checking")
    # For now, assume that we're just scanning the current directory. Add code
    # for file paths and possibly URLs at a future date ...
    scan_directory(
        "./",
        args.skip_path,
        args.create_github_issue,
        args.assign_github_issue,
        args.github_access_token)

    # Before we produce a list of unreferenced files, mark the obvious files
    # as referenced ... this is a bit hacky there 
    for file in PROTECTED_FILES:
        reference_file(file)

    if len(ALL_FILES) == 0:
        print("All files are referenced.")
    else:
        print("The following files do not appear to be referenced:")
        size = 0
        for unref in ALL_FILES:
            print(unref)
            size += os.path.getsize(unref)
        print(f"Possible size to reclaim: {size/1024**2}MB")
