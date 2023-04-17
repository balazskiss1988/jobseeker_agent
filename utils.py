import requests

def getJobs(query):
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
        "limit": 10,
        "highlightMatches": 0,
        "sort": "date",
        "query": query
    }
    response = requests.get("https://api-pro.persgroep.digital/api/v3/sites/nationalevacaturebank.nl/jobs", headers=headers, params=params)
    jobs = response.json()["_embedded"]["jobs"]
    return list(map(lambda d: {'title': d['title'], 'description': d['description']}, jobs))

print(getJobs())