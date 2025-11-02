# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['DesktopBMO.py'],
    pathex=[],
    binaries=[],
    datas=[('BMO_walking_right.gif', '.'), ('BMO_walking_left.gif', '.'), ('BMO_idle.gif', '.'), ('BMO_jumping.gif', '.'), ('BMO_sleeping.gif', '.'), ('BMO_waving.gif', '.'), ('BMO_blinking.gif', '.'), ('BMO_dragging.gif', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DesktopBMO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
