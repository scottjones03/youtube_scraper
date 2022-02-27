$convertDir = "ytapi"
./activate_venv.ps1
python -c @"
import pathlib, subprocess
for uipath in pathlib.Path().glob('$convertDir/**/*.ui'):
    pypath = uipath.parent / 'ui' / uipath.with_suffix('.py').name
    pypath.parent.mkdir(exist_ok=True, parents=True)
    (pypath.parent / '__init__.py').touch()
    if pypath.exists() and pypath.stat().st_mtime > uipath.stat().st_mtime:
        print('Up-to-date:', uipath, pypath)
    else:
        print('Converting:', uipath, pypath)
        subprocess.run(['pyside2-uic', uipath, '-o', pypath])
        data = pypath.read_text()
        data = '# pylint: disable=all\n' + data
        pypath.write_text(data)
"@