# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import copy_metadata

# 获取 Python 核心 DLL
py_version = f"{sys.version_info.major}{sys.version_info.minor}"
python_dll = f"python{py_version}.dll"

block_cipher = None

# 把 imageio 等库的元数据（版本信息）强制打包进去
meta_datas = []
meta_datas += copy_metadata('imageio')
meta_datas += copy_metadata('imgaug')
meta_datas += copy_metadata('paddleocr')

a = Analysis(
    ['d:/zmd/auto_clicker.py'],
    pathex=[],
    binaries=[],
    datas=meta_datas, 
    hiddenimports=[
        'paddleocr',
        'paddle.nn.layer.layers',
        'skimage.filters.edges',
        'skimage.morphology._skeletonize',
        'imgaug',
        'imageio',
        'shapely',
        'shapely.geometry',
        'pyclipper',
        # 🟢 解决当前的报错，并预判未来可能报错的所有依赖！
        'lmdb',
        'cv2',
        'numpy',
        'PIL',
        'PIL.Image',
        'bidi.algorithm',
        'arabic_reshaper',
        'rapidfuzz',
        'Polygon',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # 排除不需要的大型组件以减小体积
    excludes=['matplotlib', 'notebook', 'share', 'PyQt5', 'PyQt6', 'test'],
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
    name='auto_clicker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[
        'vcruntime140.dll',
        python_dll,
        'paddle_inference.dll',
        'libiomp5md.dll',
        'mkl_rt.2.dll',
        'mkl_core.2.dll',
        'mkl_intel_thread.2.dll'
    ],
    name='终末地抢单小助手',
)