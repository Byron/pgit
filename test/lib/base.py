"""Provide base classes for the test system"""
from test.testlib import TestBase

__all__ = ['TestCmdBase']

class TestCmdBase(TestBase):
	"""Foundation class from which all command test should derive to obtain
	command-specific testing utilities"""
	pass
