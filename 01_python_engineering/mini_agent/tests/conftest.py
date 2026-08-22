"""Make the standalone learning example importable from repository-root tests."""

import sys
from pathlib import Path


MINI_AGENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MINI_AGENT_DIR))
