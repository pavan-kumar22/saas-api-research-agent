import os
import pandas as pd

from search import search_docs
from extract import extract_information
from verify import verify_row

# -------------------------------------------------------
# Create output folder
# -------------------------------------------------------

os.makedirs("output", exist_ok=True)

OUTPUT_FILE = "output/research.csv"

# -------------------------------------------------------
# Read apps
# -------------------------------------------------------

apps = pd.read_csv("data/apps.csv")

# Uncomment for testing
# apps = apps.head(3)

# -------------------------------------------------------
# Resume previous run
# -------------------------------------------------------

if os.path.exists(OUTPUT_FILE):

    existing = pd.read_csv(OUTPUT_FILE)

    results = existing.to_dict("records")

    processed = set(existing["app"])

    apps = apps[~apps["name"].isin(processed)]

    print(f"Skipping {len(processed)} completed apps...\n")

else:

    results = []

# -------------------------------------------------------
# Research Loop
# -------------------------------------------------------

for _, row in apps.iterrows():

    app = row["name"]

    print("=" * 70)
    print(f"Researching: {app}")
    print("=" * 70)

    # ---------------------------------------------------
    # Search
    # ---------------------------------------------------

    search_results = search_docs(app)

    if not search_results:

        print(f"Skipping {app} (No search results)\n")

        data = {
            "category": "Unknown",
            "description": "Search Failed",
            "authentication": "Unknown",
            "self_serve": "Unknown",
            "api_surface": "Unknown",
            "mcp": "Unknown",
            "buildability": "Low",
            "blocker": "Search Failed",
            "evidence": "",
            "verified": "No",
            "confidence": "Low",
            "verification_notes": "No search results",
            "app": app
        }

        results.append(data)

        pd.DataFrame(results).to_csv(
            OUTPUT_FILE,
            index=False
        )

        continue

    # ---------------------------------------------------
    # Top URLs
    # ---------------------------------------------------

    urls = []

    print("\nTop Documentation URLs:\n")

    for result in search_results[:3]:

        print(result["href"])

        urls.append(result["href"])

    print()

    # ---------------------------------------------------
    # Extraction
    # ---------------------------------------------------

    try:

        data = extract_information(app, urls)

    except Exception as e:

        print(f"Extraction Failed ({app})")
        print(e)

        data = {
            "category": "Unknown",
            "description": "Extraction Failed",
            "authentication": "Unknown",
            "self_serve": "Unknown",
            "api_surface": "Unknown",
            "mcp": "Unknown",
            "buildability": "Low",
            "blocker": "LLM Error",
            "evidence": urls[0] if urls else ""
        }

    # ---------------------------------------------------
    # Verification
    # ---------------------------------------------------

    try:

        verification = verify_row(data)

        data["verified"] = verification["verified"]
        data["confidence"] = verification["confidence"]
        data["verification_notes"] = verification["verification_notes"]

    except Exception as e:

        print("Verification Failed")
        print(e)

        data["verified"] = "Needs Review"
        data["confidence"] = "Low"
        data["verification_notes"] = str(e)

    # ---------------------------------------------------
    # Final Row
    # ---------------------------------------------------

    data["app"] = app

    results.append(data)

    print("\nResearch Result\n")
    print(data)
    print()

    # ---------------------------------------------------
    # Save after every app
    # ---------------------------------------------------

    pd.DataFrame(results).to_csv(
        OUTPUT_FILE,
        index=False
    )

# -------------------------------------------------------
# Final Save
# -------------------------------------------------------

pd.DataFrame(results).to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("=" * 70)
print("Research Saved Successfully")
print("=" * 70)