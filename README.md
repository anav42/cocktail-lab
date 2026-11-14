# Cocktail Lab

A searchable, photo-first collection of reconstructed cocktails from real bar experiences.

**Website:** https://anav42.github.io/cocktail-lab/

## Add an original photograph

1. Open the cocktail on the website and select **Add your photo**.
2. Sign into GitHub, enter the displayed Cocktail ID, and drag/paste the photo into the Photo field.
3. Submit the issue. A GitHub Actions workflow downloads the attachment, auto-rotates and resizes it to at most 1600 × 2000 pixels, saves a quality-85 WebP in `images/<cocktail-id>/cocktail.webp`, and updates `data/recipes.json`.
4. GitHub Pages deploys the updated gallery.

Photo submissions must be photographs you own or have permission to publish. Photos are publicly accessible because the repository and site are public. Do not submit sensitive/private media. Original video files are not stored.

The processing workflow uses `scripts/process_photo_issue.py`. It accepts one GitHub-hosted image per issue, maximum 15 MB. Additional photos can be supported later.

**Important:** The photo intake workflow uses a GitHub issue form, not a direct upload from ChatGPT. ChatGPT can still develop and save recipe text, but private chat attachments do not automatically become GitHub-hosted attachments.

## Recipe data

`data/recipes.json` is the source of truth. The website groups recipes by base spirit and sorts alphabetically within each group. Recipes distinguish original observations from experimental quantities and methods.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
