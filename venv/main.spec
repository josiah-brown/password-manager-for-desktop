# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/josiahbrown/PycharmProjects/day-29-password-manager','/Users/josiahbrown/PycharmProjects/day-29-password-manager/venv/lib/python3.9/site-packages','/Users/josiahbrown/PycharmProjects/day-29-password-manager/venv/lib/python3.9/site-packages/PyInstaller'],
             binaries=[],
             datas=[('logo.png','.')],
             hiddenimports=['pyperclip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='main.app',
             icon=None,
             bundle_identifier=None)
