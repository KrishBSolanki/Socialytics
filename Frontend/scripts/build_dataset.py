"""Convert the Zenodo CSR Brand Posts dataset (record 22042887, CC BY 4.0)
into compact JSON served from public/data. Run: python3 scripts/build_dataset.py
Source CSVs are downloaded to /tmp/ds if missing. No values are invented."""
import json, os, re, unicodedata, urllib.request
import pandas as pd

SRC = "https://zenodo.org/api/records/22042887/files/{}/content"
TMP = "/tmp/ds"
OUT = os.path.join(os.path.dirname(__file__), "..", "public", "data")
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
for name, local in [("brands_posts.csv", "posts.csv"), ("brands_comments.csv", "comments.csv")]:
    path = os.path.join(TMP, local)
    if not os.path.exists(path):
        urllib.request.urlretrieve(SRC.format(name), path)

def slug(s):
    s = s.replace("ı", "i").replace("İ", "I")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def num(v):
    return None if pd.isna(v) else (int(v) if float(v).is_integer() else float(v))

p = pd.read_csv(os.path.join(TMP, "posts.csv"), dtype={"Tweet ID": str})
c = pd.read_csv(os.path.join(TMP, "comments.csv"), dtype={"Tweet ID": str, "parent": str})
EMO = ["anger", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
posts = []
for r in p.itertuples(index=False):
    d = r._asdict()
    row = p.columns
    rec = dict(zip(row, r))
    emotions = None if pd.isna(rec["sampled_comments"]) else {e: int(rec[e]) for e in EMO}
    posts.append({
        "id": rec["Tweet ID"], "ts": pd.Timestamp(rec["Timestamp"]).isoformat(),
        "brand": rec["Brand"], "brandId": slug(rec["Brand"]),
        "nationality": rec["Nationality"], "industry": rec["Industry"],
        "followers": int(rec["FollowersCount"]),
        "isReply": bool(rec["is_reply"]), "isRetweet": bool(rec["is_retweet"]),
        "image": bool(rec["image"]), "video": bool(rec["video"]),
        "postType": rec["brand_post_type"],
        "aidAction": None if pd.isna(rec["disaster_aid_action_type"]) else rec["disaster_aid_action_type"],
        "reliefEffect": rec["relief_effect_type"],
        "comments": num(rec["Comments"]), "retweets": num(rec["Retweets"]), "likes": num(rec["Likes"]),
        "tags": int(rec["tag_count"]), "mentions": int(rec["mention_count"]),
        "emojis": int(rec["emoji_count"]), "urls": int(rec["url_count"]),
        "period": rec["disaster_period"], "emotions": emotions,
        "sampledComments": None if pd.isna(rec["sampled_comments"]) else int(rec["sampled_comments"]),
    })
comments = [[r["Tweet ID"], pd.Timestamp(r["Timestamp"]).isoformat(), r["parent"], r["predicted_label"]]
            for r in c.to_dict("records")]
meta = {
    "title": "CSR Communication of Local and Global Brands During the February 6, 2023 Türkiye Earthquakes: Platform X Posts and Public Engagement Data",
    "doi": "10.5281/zenodo.22042887", "url": "https://zenodo.org/records/22042887",
    "license": "CC BY 4.0", "authors": ["Altug Tanaltay", "Raha Akhavan-Tabatabaei"],
    "publisher": "Sabancı University", "platform": "X (formerly Twitter)",
    "coverage": {"start": "2023-01-01", "end": "2023-03-30"}, "eventDate": "2023-02-06",
    "files": [
        {"name": "brands_posts.csv", "rows": len(p), "columns": [{"name": col, "missing": int(p[col].isna().sum()), "dtype": str(p[col].dtype)} for col in p.columns]},
        {"name": "brands_comments.csv", "rows": len(c), "columns": [{"name": col, "missing": int(c[col].isna().sum()), "dtype": str(c[col].dtype)} for col in c.columns]},
    ],
}
json.dump(posts, open(os.path.join(OUT, "posts.json"), "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(comments, open(os.path.join(OUT, "comments.json"), "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), ensure_ascii=False, indent=1)
print(len(posts), len(comments))
