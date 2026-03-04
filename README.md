# Are.na → Google Slides

Download all images from an [Are.na](https://www.are.na/) channel and turn them into a Google Slides presentation — one image per slide on a dark gray background.

## How it works

1. **Downloads** all images from an Are.na channel via the public API
2. **Builds** a 16:9 PowerPoint deck (dark gray `#333` background, images scaled to fit)
3. **Uploads** to Google Drive via `rclone`, converting to Google Slides

## Quick start

### Double-click (macOS)

Double-click `Arena to Slides.command`. A dialog will ask for the channel URL, then Terminal shows progress. A notification appears when it's done.

### Command line

```bash
python arena_to_slides.py https://www.are.na/james-hicks/baroque-user-interface
python arena_to_slides.py baroque-user-interface
python arena_to_slides.py  # interactive prompt
```

### Download images only

```bash
python download_arena_images.py baroque-user-interface
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-pptx Pillow
```

### Connecting Google Drive

The upload step uses [rclone](https://rclone.org/) to copy the `.pptx` into your Google Drive, where it's automatically converted to a Google Slides presentation.

1. Install rclone:
   ```bash
   brew install rclone
   ```

2. Create a Google Drive remote called `gdrive`:
   ```bash
   rclone config
   ```
   - Choose **n** (New remote)
   - Name it **gdrive**
   - Choose **Google Drive** from the list (type `drive`)
   - Leave Client ID and Client Secret blank (press Enter for defaults)
   - Scope: choose **1** (full access)
   - Leave root folder and service account blank (press Enter)
   - Auto config: choose **Y** — a browser window will open asking you to sign in to Google and authorize rclone
   - Team Drive: choose **N** (unless you want a shared drive)
   - Confirm with **Y**

3. Verify it works:
   ```bash
   rclone ls gdrive: --max-depth 1
   ```
   You should see files from your Google Drive root.

If you skip this step, everything still works — the `.pptx` file is saved locally and you can open or upload it manually.

## Files

| File | Description |
|---|---|
| `arena_to_slides.py` | Full pipeline: download → slideshow → upload |
| `download_arena_images.py` | Standalone image downloader |
| `make_slides.py` | Standalone slideshow builder |
| `Arena to Slides.command` | macOS double-click launcher |
