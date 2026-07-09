import json
import pandas as pd
from pathlib import Path

INPUT_FILE = "output/research.csv"
OUTPUT_FILE = "output/insights.json"


def percentage(series):

    counts = series.fillna("Unknown").value_counts()

    total = len(series)

    return {
        str(k): round((v / total) * 100, 2)
        for k, v in counts.items()
    }


def top_easy_wins(df):

    easy = df[
        (df["buildability"] == "High") &
        (df["self_serve"] == "Yes")
    ]

    if "authentication" in easy.columns:
        easy = easy.sort_values(
            by=["authentication", "app"]
        )

    return easy["app"].head(5).tolist()


def enterprise_gated(df):

    blockers = df["blocker"].fillna("").str.lower()

    gated = blockers.str.contains(
        "enterprise|partner|paid|admin|approval"
    )

    return {
        "count": int(gated.sum()),
        "percentage": round(
            gated.mean() * 100,
            2
        )
    }


def verification_summary(df):

    if "verified" not in df.columns:

        return {}

    return {
        "verified": percentage(df["verified"]),
        "confidence": percentage(df["confidence"])
    }


def main():

    if not Path(INPUT_FILE).exists():

        print("research.csv not found.")

        return

    df = pd.read_csv(INPUT_FILE)

    insights = {

        "total_apps": len(df),

        "authentication_percent": percentage(
            df["authentication"]
        ),

        "category_percent": percentage(
            df["category"]
        ),

        "buildability_percent": percentage(
            df["buildability"]
        ),

        "self_serve_percent": percentage(
            df["self_serve"]
        ),

        "api_surface_percent": percentage(
            df["api_surface"]
        ),

        "mcp_support_percent": percentage(
            df["mcp"]
        ),

        "common_blockers": percentage(
            df["blocker"]
        ),

        "enterprise_gated": enterprise_gated(df),

        "top_5_easy_wins": top_easy_wins(df),

        "verification": verification_summary(df)

    }

    Path(OUTPUT_FILE).parent.mkdir(
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            insights,
            f,
            indent=4
        )

    print("=" * 60)
    print("Insights Generated")
    print("=" * 60)

    print(json.dumps(
        insights,
        indent=4
    ))

    print()
    print(f"Saved -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()