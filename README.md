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

For Google Drive upload:

```bash
brew install rclone
rclone config create gdrive drive
```

If `rclone` is not installed, the `.pptx` file is saved locally and can be opened directly.

## Files

| File | Description |
|---|---|
| `arena_to_slides.py` | Full pipeline: download → slideshow → upload |
| `download_arena_images.py` | Standalone image downloader |
| `make_slides.py` | Standalone slideshow builder |
| `Arena to Slides.command` | macOS double-click launcher |
