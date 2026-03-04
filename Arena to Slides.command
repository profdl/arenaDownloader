#!/bin/bash
# Double-click this file to launch the Are.na → Google Slides pipeline.
# A popup will ask for the channel URL, then Terminal shows progress.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Show a popup dialog asking for the URL
URL=$(osascript -e '
tell application "System Events"
    activate
    set dialogResult to display dialog "Paste an Are.na channel URL:" default answer "https://www.are.na/" with title "Are.na → Google Slides" buttons {"Cancel", "Go"} default button "Go" with icon note
    return text returned of dialogResult
end tell
' 2>/dev/null)

# Exit if user cancelled
if [ -z "$URL" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "╭──────────────────────────────────────────╮"
echo "│  Are.na → Google Slides                  │"
echo "╰──────────────────────────────────────────╯"
echo ""
echo "Channel: $URL"
echo ""

# Run with venv Python directly (more reliable than source activate in .command files)
"$SCRIPT_DIR/.venv/bin/python3" "$SCRIPT_DIR/arena_to_slides.py" "$URL"

# Show a macOS notification when done
osascript -e 'display notification "Your slides are in Google Drive." with title "Are.na → Google Slides" sound name "Glass"' 2>/dev/null

echo ""
echo "Press any key to close this window."
read -n 1 -s
