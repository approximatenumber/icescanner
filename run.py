#!/usr/bin/env python3

from lib.entrypoint import Entrypoint


entrypoint = Entrypoint()
entrypoint.do_diagnostics()
entrypoint.take_shot()
entrypoint.stop()
