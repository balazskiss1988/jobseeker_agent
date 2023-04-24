import requests


def parse_action(string: str):
    assert string.startswith("action:")
    idx = string.find("action_input=")
    if idx == -1:
        return string[8:], None
    return string[8: idx - 1], string[idx + 13:].strip("'").strip('"')


def get_jobs(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "x-destination": "job-service",
        "x-source": "Job Board NationaleVacaturebank.nl",
        "Origin": "https://www.nationalevacaturebank.nl",
        "Connection": "keep-alive",
        "Referer": "https://www.nationalevacaturebank.nl/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailers",
    }
    params = {
        "page": 1,
        "limit": 1,
        "highlightMatches": 0,
        "sort": "date",
        "query": query
    }
    response = requests.get("https://api-pro.persgroep.digital/api/v3/sites/nationalevacaturebank.nl/jobs",
                            headers=headers, params=params)
    jobs = response.json()["_embedded"]["jobs"]
    return list(map(lambda d: {'id': d['id'], 'title': d['title'], 'description': d['description']}, jobs))


def key_exist_and_not_blank(dictionary, key):
    return key in dictionary and dictionary[key] != ''


def format_memory(memory):
    text = ""
    if key_exist_and_not_blank(memory, 'current_user_response'):
        text += "\nThe user has responded with: " + memory['current_user_response']
    if key_exist_and_not_blank(memory, 'current_job'):
        text += "\nThe current job to be shown to the user is: " + memory['current_job']
    if 'found_jobs' in memory and len(memory['found_jobs']) > 0:
        text += "\nThe jobs found so far are: " + ' '.join(memory['found_jobs'])
    if key_exist_and_not_blank(memory, 'title'):
        text += "\nThe jobsekeer's preferred job title is: " + memory['title']
    return text
