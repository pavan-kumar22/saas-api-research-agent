import requests
import pandas as pd
from urllib.parse import urlparse

INPUT_FILE = "output/research.csv"
OUTPUT_FILE = "output/verified.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

OFFICIAL_DOMAINS = [
    "developer.salesforce.com",
    "docs.github.com",
    "docs.slack.dev",
    "api.slack.com",
    "developer.atlassian.com",
    "developers.notion.com",
    "stripe.com",
    "developer.xero.com",
    "developer.intuit.com",
]


def download_page(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )

        return response.status_code, response.text.lower()

    except Exception:

        return None, ""


def verify_row(row):

    verification = {
        "verified": "Yes",
        "confidence": "High",
        "verification_notes": ""
    }

    notes = []

    url = str(row["evidence"]).strip()

    domain = urlparse(url).netloc.lower()

    status, page = download_page(url)

    # -------------------------------------------------------
    # URL unreachable
    # -------------------------------------------------------

    if status is None:

        verification["verified"] = "No"
        verification["confidence"] = "Low"

        notes.append("Evidence URL unreachable")

    # -------------------------------------------------------
    # Official docs blocked
    # -------------------------------------------------------

    elif status == 403 and domain in OFFICIAL_DOMAINS:

        verification["verified"] = "Needs Review"
        verification["confidence"] = "Medium"

        notes.append(
            "Official documentation blocks automated access (403)"
        )

    # -------------------------------------------------------
    # HTTP Error
    # -------------------------------------------------------

    elif status != 200:

        verification["verified"] = "No"
        verification["confidence"] = "Low"

        notes.append(f"HTTP {status}")

    else:

        auth = str(row["authentication"]).lower()

        if auth == "oauth2":

            if "oauth" not in page:

                verification["confidence"] = "Medium"

                notes.append(
                    "OAuth not explicitly found"
                )

        elif auth == "api key":

            if "api key" not in page:

                verification["confidence"] = "Medium"

                notes.append(
                    "API Key not explicitly found"
                )

        elif auth == "bearer token":

            if "bearer" not in page:

                verification["confidence"] = "Medium"

                notes.append(
                    "Bearer token not explicitly found"
                )

        surface = str(row["api_surface"]).lower()

        if "rest" in surface:

            if "rest" not in page:

                verification["confidence"] = "Medium"

                notes.append(
                    "REST not explicitly found"
                )

        if "graphql" in surface:

            if "graphql" not in page:

                verification["confidence"] = "Medium"

                notes.append(
                    "GraphQL not explicitly found"
                )

        if "soap" in surface:

            if "soap" not in page:

                verification["confidence"] = "Medium"

                notes.append(
                    "SOAP not explicitly found"
                )

    # -------------------------------------------------------
    # Convert list -> string
    # -------------------------------------------------------

    verification["verification_notes"] = "; ".join(notes)

    return verification


def main():

    df = pd.read_csv(INPUT_FILE)

    sample_size = min(15, len(df))

    sample = df.sample(
        n=sample_size,
        random_state=42
    ).copy()

    verified_rows = []

    print("=" * 60)
    print("VERIFYING SAMPLE")
    print("=" * 60)

    for _, row in sample.iterrows():

        print(row["app"])

        result = verify_row(row)

        row = row.copy()

        row["verified"] = result["verified"]
        row["confidence"] = result["confidence"]
        row["verification_notes"] = result["verification_notes"]

        verified_rows.append(row)

    verified_df = pd.DataFrame(verified_rows)

    verified_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 60)
    print("Verification Complete")
    print("=" * 60)
    print(f"Saved -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()