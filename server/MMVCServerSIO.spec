# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['MMVCServerSIO.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('C:\\Users\\whousethispc\\anaconda3\\envs\\mmvc-server\\Lib\\site-packages\\fairseq', '.\\fairseq'),
    ('C:\\Users\\whousethispc\\Desktop\\master\\Voice Changer Projectttt\\voice-changer222\\client\\demo\\dist', '.\\dist'),
    ('C:\\Users\\whousethispc\\Desktop\\master\\Voice Changer Projectttt\\voice-changer222\\server\\pretrain', '.\\pretrain'),

    ],
    hiddenimports=[],
    hookspath=['./extra-hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MMVCServerSIO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MMVCServerSIO',
)
