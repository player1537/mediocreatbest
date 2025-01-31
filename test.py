"""

"""

from __future__ import annotations
from mediocreatbest import auto


def test_versions_identical():
    def version(s: str) -> tuple[int, int, int, int | None]:
        # python version: e.g. 3.10.0b1
        if match := auto.re.match(r'(\d+)\.(\d+)\.(\d+)(?:([ab])(\d+))?', s):
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            pre = match.group(4)
            pre_num = int(match.group(5)) if pre else None
            return major, minor, patch, pre_num

        # js version: e.g. 3.10.0-alpha.1
        if match := auto.re.match(r'(\d+)\.(\d+)\.(\d+)(?:-(\w+)\.(\d+))?', s):
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            pre = match.group(4)
            pre_num = int(match.group(5)) if pre else None
            return major, minor, patch, pre_num
    
        assert False, f'Invalid version string: {s}'
        
    root = auto.pathlib.Path(__file__).parent
    
    path = root / 'metadata.json'
    metadata = auto.json.loads(path.read_text())

    path = root / 'js' / 'package.json'
    package = auto.json.loads(path.read_text())

    path = root / 'py' / 'pyproject.toml'
    pyproject = auto.toml.loads(path.read_text())
    
    assert version(metadata['version']) == version(package['version']) == version(pyproject['project']['version'])

