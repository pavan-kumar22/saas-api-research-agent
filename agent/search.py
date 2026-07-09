from ddgs import DDGS
from ddgs.exceptions import DDGSException

# ----------------------------------------------------
# Domains to avoid
# ----------------------------------------------------

BAD_DOMAINS = [
    "reddit.com",
    "medium.com",
    "youtube.com",
    "stackoverflow.com",
    "postman.com",
    "apitracker.io",
    "namespacecomm",
    "github.com",
    "blog",
]

# ----------------------------------------------------
# Score Search Result
# ----------------------------------------------------


def score_result(result):

    url = result.get("href", "").lower()

    score = 0

    # Prefer official documentation

    if "developers." in url:
        score += 1000

    if "developer." in url:
        score += 1000

    if "docs." in url:
        score += 950

    if "/developers/" in url:
        score += 900

    if "/developer/" in url:
        score += 900

    if "/docs/" in url:
        score += 850

    if "/apis/" in url:
        score += 750

    if "/api/" in url:
        score += 700

    if "/rest" in url:
        score += 600

    if "/graphql" in url:
        score += 600

    if "reference" in url:
        score += 400

    # Penalize unwanted domains

    for bad in BAD_DOMAINS:
        if bad in url:
            score -= 2000

    return score


# ----------------------------------------------------
# Search Official Documentation
# ----------------------------------------------------


def search_docs(app_name):

    query = f"{app_name} official developer API documentation"

    # -----------------------------
    # Search
    # -----------------------------

    try:

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=10))

    except DDGSException:

        print(f"No search results for {app_name}")
        return []

    except Exception as e:

        print(f"Search Error ({app_name}): {e}")
        return []

    # -----------------------------
    # Remove invalid URLs
    # -----------------------------

    filtered = []

    for result in results:

        url = result.get("href", "").strip()

        if not url:
            continue

        # Ignore DuckDuckGo redirect links
        if url.startswith("/"):
            continue

        if "/clev" in url:
            continue

        # Ignore anything that isn't HTTP/HTTPS
        if not url.startswith("http"):
            continue

        filtered.append(result)

    # -----------------------------
    # Score Results
    # -----------------------------

    for result in filtered:
        result["score"] = score_result(result)

    filtered.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return filtered