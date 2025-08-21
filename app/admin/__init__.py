import sys
from pathlib import Path


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))