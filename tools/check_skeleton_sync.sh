#!/usr/bin/env bash
# Fail if the two copies of the blog-post skeleton have drifted apart.
#
# `.github/ISSUE_TEMPLATE/blog-post.md` is canonical: GitHub's issue-template chooser only
# reads that directory. `docs/templates/blog-post-skeleton.md` is a byte-identical copy,
# because intake path C needs a file a contributor can download and attach, and a symlink
# does not survive raw.githubusercontent.com.
#
# See AGENTS.md, "The skeleton exists twice, on purpose".

set -euo pipefail

CANONICAL=".github/ISSUE_TEMPLATE/blog-post.md"
COPY="docs/templates/blog-post-skeleton.md"

# Neither file exists yet (or one is being introduced in a later commit): nothing to check.
if [ ! -f "$CANONICAL" ] && [ ! -f "$COPY" ]; then
    exit 0
fi

if [ ! -f "$CANONICAL" ]; then
    echo "ERROR: $COPY exists but the canonical $CANONICAL does not." >&2
    exit 1
fi

if [ ! -f "$COPY" ]; then
    echo "ERROR: $CANONICAL exists but its copy $COPY does not." >&2
    echo "  Fix: cp $CANONICAL $COPY" >&2
    exit 1
fi

if ! cmp -s "$CANONICAL" "$COPY"; then
    echo "" >&2
    echo "========================================================================" >&2
    echo "  The two copies of the blog-post skeleton have drifted." >&2
    echo "  $CANONICAL is canonical." >&2
    echo "" >&2
    echo "  Fix: cp $CANONICAL $COPY" >&2
    echo "========================================================================" >&2
    echo "" >&2
    diff -u "$COPY" "$CANONICAL" >&2 || true
    exit 1
fi
