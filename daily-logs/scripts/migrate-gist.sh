#!/bin/bash

# Daily Log Migration Script
# Migrates daily log from gist to repository structure
# This script is for historical reference - migration already completed

set -e

GIST_ID="5e2da7e26d47e0e734935cdcdbb1df73"
REPO_DIR="/Users/nsteffens/.claude"
DAILY_LOGS_DIR="$REPO_DIR/daily-logs"

echo "🔄 Starting daily log migration from gist to repository..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$DAILY_LOGS_DIR/2025"
mkdir -p "$DAILY_LOGS_DIR/scripts"

# Download gist content
echo "⬇️  Downloading gist content..."
gh gist view "$GIST_ID" --raw > /tmp/daily-log-full.md

# Note: Actual parsing and splitting was done manually
# This script serves as documentation of the migration process

echo "✅ Migration completed!"
echo "📊 Migration summary:"
echo "   - Source: Gist $GIST_ID"
echo "   - Target: $DAILY_LOGS_DIR"
echo "   - Structure: Yearly directories with monthly files"
echo "   - Template: Extracted to template.md"
echo "   - Total entries: 12 date sections migrated"

echo ""
echo "🔗 Next steps:"
echo "   1. Update /daily-log command to use new structure"
echo "   2. Test new workflow with next session"
echo "   3. Mark gist as deprecated"
echo "   4. Update documentation"

echo ""
echo "📂 New structure:"
echo "   daily-logs/"
echo "   ├── README.md"
echo "   ├── template.md"
echo "   ├── 2025/"
echo "   │   ├── 2025-08.md"
echo "   │   └── index.md"
echo "   └── scripts/"
echo "       └── migrate-gist.sh"