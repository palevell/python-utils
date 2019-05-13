#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# debug_utils/__init__.py - Friday, April 12, 2019
__version__ = '1.1.6'

from dataclasses import dataclass
from enum import Enum, auto
from os.path import basename, splitext
from threading import Lock
from time import sleep
import sys

__MODULE__ = splitext(basename(__file__))[0]

DRY_RUN     = True
DEBUG       = True
ENVIRONMENT = 'Development'

lock = Lock()

class TraceDirection(Enum):
	In  = auto()
	Out = auto()

class Verbosity(Enum):
	Errors      = auto()
	Warnings    = auto()
	Information = auto()
	Debug       = auto()
	Trace       = auto()

@dataclass()
class DebugLog:
	_class_sig:     str = __MODULE__ + '.DebugLog'
	_trace_level:   int = 0
	verbosity:      Verbosity = Verbosity.Trace

	def __post_init__(self):
		self._proc_stack = []

	def _prefix(self):
		return '  ' * self._trace_level

	def _enter_exit(self, proc_sig, direction, memo=None):
		"""
		:param proc_sig: Procedure signature
		:param direction: IN/OUT
		:param memo: ex. Tweet ID or return value
		:return:
		"""
		_proc_sig = self._class_sig + '.enter_exit()'
		if memo:
			msg = '%s %s' % (proc_sig, memo)
		else:
			msg = '%s' % proc_sig
		with lock:
			if direction == TraceDirection.In:
				print("%sEntering %s" % (self._prefix(), msg))
			elif direction == TraceDirection.Out:
				print("%sExiting  %s" % (self._prefix(), msg))
			sleep(1)

	def enter(self, proc_sig, memo=None):
		self._proc_stack.append(proc_sig)
		if self.verbosity.value == Verbosity.Trace.value:
			self._enter_exit(proc_sig, TraceDirection.In, memo)
			self._trace_level += 1

	def exit(self, memo=None):
		if self.verbosity.value == Verbosity.Trace.value:
			self._trace_level -= 1
			self._enter_exit(self.current_proc, TraceDirection.Out, memo)
		self._proc_stack.pop()

	@property
	def current_proc(self):
		return self._proc_stack[-1:][0]

	def print(self, *args, **kwargs):
		if self.verbosity.value >= Verbosity.Information.value:
			print(self._prefix()[:-1], self.current_proc, *args, **kwargs, flush=True)

	def eprint(self, *args, **kwargs):
		if self.verbosity.value >= Verbosity.Errors.value:
			print(self._prefix()[:-1], self.current_proc, *args, **kwargs, file=sys.stderr, flush=True)

if __name__ == '__main__':
	dlog = DebugLog()
	print(dlog.verbosity)
	dlog.enter('test1')
	dlog.enter('test2')
	print(dlog.current_proc)
	dlog.exit()
	print(dlog.current_proc)
