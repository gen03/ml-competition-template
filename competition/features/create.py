#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

import pandas as pd

from .base import get_arguments, generate_features


def create_features():
    args = get_arguments()
    generate_features(globals(), args.force)


if __name__ == '__main__':
    create_features()
