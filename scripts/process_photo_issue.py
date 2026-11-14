"""Process a GitHub issue-form photo into the Cocktail Lab public gallery."""
import io
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
body = event["issue"].get("body") or ""
match = re.search(r"### Cocktail ID\s+([^\n]+)", body)
if not match:
    raise SystemExit("Missing Cocktail ID field")
cocktail_id = match.group(1).strip().strip("`").lower()
if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", cocktail_id):
    raise SystemExit("Invalid cocktail ID")
catalog_path = ROOT / "data" / "recipes.json"
catalog = json.loads(catalog_path.read_text())
recipe = next((r for r in catalog["recipes"] if r["id"] == cocktail_id), None)
if recipe is None:
    raise SystemExit("No recipe with that ID exists")
photo_section = body.split("### Photo", 1)[-1].split("### Permission", 1)[0]
urls = re.findall(r"https://[^\s)<>]+", photo_section)
allowed = ("github.com", "user-images.githubusercontent.com", "githubusercontent.com")
urls = [u for u in urls if urllib.parse.urlparse(u).hostname in allowed]
if not urls:
    raise SystemExit("No GitHub-hosted attachment found in Photo field")
url = urls[0]
request = urllib.request.Request(url, headers={"User-Agent": "CocktailLabPhotoProcessor/1.0"})
with urllib.request.urlopen(request, timeout=25) as response:
    if int(response.headers.get("Content-Length", "0")) > 15_000_000:
        raise SystemExit("Image exceeds 15 MB limit")
    raw = response.read(15_000_001)
if len(raw) > 15_000_000:
    raise SystemExit("Image exceeds 15 MB limit")
try:
    image = Image.open(io.BytesIO(raw))
    image.verify()
    image = Image.open(io.BytesIO(raw))
except (UnidentifiedImageError, OSError) as exc:
    raise SystemExit("Attachment is not a supported image") from exc
image = ImageOps.exif_transpose(image).convert("RGB")
image.thumbnail((1600, 2000), Image.Resampling.LANCZOS)
destination = ROOT / "images" / cocktail_id
destination.mkdir(parents=True, exist_ok=True)
path = destination / "cocktail.webp"
image.save(path, "WEBP", quality=85, method=6)
relative = "./images/" + cocktail_id + "/cocktail.webp"
recipe["image"] = relative
recipe["images"] = [relative]
catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write("changed=true\n")
print(f"Saved {path.relative_to(ROOT)} ({image.width}x{image.height})")
