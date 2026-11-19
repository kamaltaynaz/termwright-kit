"""EXAMPLE ONLY: a read-only Canvas call with paging, token from the environment, back-off.

Not a working tool. Placeholders: the host and course id below are invented.
"""
import os
import re
import time

import requests

BASE = "https://canvas.example.edu"          # placeholder host
MAX_REQUESTS = 200                           # a cap per run, always


def get_all(path, params=None):
    token = os.environ["CANVAS_TOKEN"]       # never hard-code, never print
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    url, results, requests_made = BASE + path, [], 0
    while url:
        if requests_made >= MAX_REQUESTS:
            raise RuntimeError("request cap reached: partial result, do not draw conclusions")
        resp = session.get(url, params=params, timeout=30)
        requests_made += 1
        if resp.status_code in (403, 429):   # throttled: wait, then try this page again
            time.sleep(5)
            continue
        params = None                        # the "next" link already carries them
        resp.raise_for_status()
        results.extend(resp.json())
        remaining = float(resp.headers.get("X-Rate-Limit-Remaining", "700"))
        if remaining < 50:                   # slow down before being slowed down
            time.sleep(2)
        links = resp.headers.get("Link", "")
        match = re.search(r'<([^>]+)>;\s*rel="next"', links)
        url = match.group(1) if match else None
    return results


if __name__ == "__main__":
    sections = get_all("/api/v1/courses/COURSE_ID/sections", {"per_page": 100})
    print(len(sections), "sections")
