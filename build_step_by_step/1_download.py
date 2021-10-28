#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2019 The ungoogled-chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
ungoogled-chromium build script for Microsoft Windows
"""

import sys
if sys.version_info.major < 3 or sys.version_info.minor < 6:
    raise RuntimeError('Python 3.6+ is required for this script. You have: {}.{}'.format(
        sys.version_info.major, sys.version_info.minor))

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'ungoogled-chromium' / 'utils'))
import downloads
import domain_substitution
import prune_binaries
import patches
from _common import ENCODING, USE_REGISTRY, ExtractorEnum, get_logger
sys.path.pop(0)

_ROOT_DIR = Path(__file__).resolve().parent

def _make_tmp_paths():
    """Creates TMP and TEMP variable dirs so ninja won't fail"""
    tmp_path = Path(os.environ['TMP'])
    if not tmp_path.exists():
        tmp_path.mkdir()
    tmp_path = Path(os.environ['TEMP'])
    if not tmp_path.exists():
        tmp_path.mkdir()


def main():
    """CLI Entrypoint"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--disable-ssl-verification',
        action='store_true',
        help='Disables SSL verification for downloading')
    parser.add_argument(
        '--7z-path',
        dest='sevenz_path',
        default=USE_REGISTRY,
        help=('Command or path to 7-Zip\'s "7z" binary. If "_use_registry" is '
              'specified, determine the path from the registry. Default: %(default)s'))
    parser.add_argument(
        '--winrar-path',
        dest='winrar_path',
        default=USE_REGISTRY,
        help=('Command or path to WinRAR\'s "winrar.exe" binary. If "_use_registry" is '
              'specified, determine the path from the registry. Default: %(default)s'))
    args = parser.parse_args()

    # Set common variables
    source_tree = _ROOT_DIR / 'build' / 'src'
    downloads_cache = _ROOT_DIR / 'build' / 'downloads_cache'
    domsubcache = _ROOT_DIR / 'build' / 'domsubcache.tar.gz'

    # Setup environment
    source_tree.mkdir(parents=True, exist_ok=True)
    downloads_cache.mkdir(parents=True, exist_ok=True)
    _make_tmp_paths()

    # Get download metadata (DownloadInfo)
    download_info = downloads.DownloadInfo([
        _ROOT_DIR / 'downloads.ini',
        _ROOT_DIR / 'ungoogled-chromium' / 'downloads.ini',
    ])

    # Retrieve downloads
    get_logger().info('Downloading required files...')
    downloads.retrieve_downloads(download_info, downloads_cache, True,
                                          args.disable_ssl_verification)
    try:
        downloads.check_downloads(download_info, downloads_cache)
    except downloads.HashMismatchError as exc:
        get_logger().error('File checksum does not match: %s', exc)
        exit(1)

    # Unpack downloads
    extractors = {
        ExtractorEnum.SEVENZIP: args.sevenz_path,
        ExtractorEnum.WINRAR: args.winrar_path,
    }
    get_logger().info('Unpacking downloads...')
    downloads.unpack_downloads(download_info, downloads_cache, source_tree, extractors)

if __name__ == '__main__':
    main()
