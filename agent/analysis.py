import pandas as pd


df = pd.read_csv("output/research.csv")

print("=" * 70)
print("AUTHENTICATION")
print("=" * 70)

print(df["authentication"].value_counts())

print()

print("=" * 70)
print("CATEGORY")
print("=" * 70)

print(df["category"].value_counts())

print()

print("=" * 70)
print("SELF SERVE")
print("=" * 70)

print(df["self_serve"].value_counts())

print()

print("=" * 70)
print("BUILDABILITY")
print("=" * 70)

print(df["buildability"].value_counts())

print()

print("=" * 70)
print("BLOCKERS")
print("=" * 70)

print(df["blocker"].value_counts())

print()

print("=" * 70)
print("CONFIDENCE")
print("=" * 70)

print(df["confidence"].value_counts())
