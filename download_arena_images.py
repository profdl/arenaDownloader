#!/usr/bin/env python3
"""
Download all images from an Are.na channel.

Usage:
    python download_arena_images.py baroque-user-interface
    python download_arena_images.py https://www.are.na/james-hicks/baroque-user-interface

Requirements:
    pip install requests
"""

import requests
import json
import os
import sys
import re
import time
from urllib.parse import urlparse

def get_slug(input_str):
    """Extract channel slug from URL or use directly."""
    if "are.na" in input_str:
        parts = input_str.rstrip("/").split("/")
        return parts[-1]
    return input_str

def download_channel_images(slug, output_dir=None):
    if output_dir is None:
        output_dir = f"arena_{slug}"
    os.makedirs(output_dir, exist_ok=True)

    base_url = f"https://api.are.na/v2/channels/{slug}/contents"
    page = 1
    per_page = 50
    downloaded = 0
    failed = 0
    total_blocks = 0

    print(f"Fetching channel: {slug}\n")

    while True:
        params = {"page": page, "per": per_page}
        resp = requests.get(base_url, params=params)

        if resp.status_code != 200:
            print(f"Error fetching page {page}: {resp.status_code}")
            print(resp.text)
            break

        data = resp.json()
        contents = data.get("contents", [])
        total = data.get("length", 0)

        if not contents:
            break

        if page == 1:
            print(f"Total blocks in channel: {total}\n")
            # Debug: dump first image block to see URL structure
            for block in contents:
                if block.get("class") == "Image":
                    print("=== Sample image block structure ===")
                    print(json.dumps(block.get("image", {}), indent=2))
                    print("====================================\n")
                    break

        for block in contents:
            total_blocks += 1
            block_class = block.get("class", "")
            block_id = block.get("id", "unknown")
            title = block.get("title") or ""

            if block_class != "Image":
                print(f"  Skipping non-image block {block_id} ({block_class}): {title[:50]}")
                continue

            image = block.get("image", {})

            # Try multiple URL sources in order of preference
            image_url = (
                image.get("original", {}).get("url")
                or image.get("large", {}).get("url")
                or image.get("display", {}).get("url")
                or image.get("thumb", {}).get("url")
            )

            if not image_url:
                # Maybe the URL is at the block level
                image_url = block.get("source", {}).get("url") if isinstance(block.get("source"), dict) else None

            if not image_url:
                print(f"  No image URL for block {block_id}. Keys in image: {list(image.keys())}")
                continue

            # Ensure URL is absolute
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            elif not image_url.startswith("http"):
                image_url = "https://images.are.na/" + image_url.lstrip("/")

            # Build filename
            ext = os.path.splitext(urlparse(image_url).path)[1] or ".jpg"
            safe_title = re.sub(r'[^\w\s-]', '', title)[:60].strip() if title else ""
            if safe_title:
                filename = f"{block_id}_{safe_title}{ext}"
            else:
                filename = f"{block_id}{ext}"
            filename = filename.replace(" ", "_")

            filepath = os.path.join(output_dir, filename)

            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                print(f"  Already exists: {filename}")
                downloaded += 1
                continue

            try:
                img_resp = requests.get(image_url, timeout=30, headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                })
                img_resp.raise_for_status()

                if len(img_resp.content) == 0:
                    print(f"  WARNING: Empty response for {block_id} from {image_url}")
                    failed += 1
                    continue

                with open(filepath, "wb") as f:
                    f.write(img_resp.content)
                downloaded += 1
                size_kb = len(img_resp.content) / 1024
                print(f"  Downloaded: {filename} ({size_kb:.1f} KB)")
            except Exception as e:
                print(f"  Failed to download {block_id}: {e}")
                print(f"    URL was: {image_url}")
                failed += 1

            # Small delay to be polite to the server
            time.sleep(0.2)

        page += 1

    print(f"\nDone! Downloaded {downloaded} images to ./{output_dir}/")
    if failed:
        print(f"Failed: {failed}")
    print(f"Processed {total_blocks} blocks total.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        channel = "baroque-user-interface"
    else:
        channel = sys.argv[1]

    slug = get_slug(channel)
    download_channel_images(slug)