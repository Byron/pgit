#-*-coding:utf-8-*-
"""
@package pgit.cmd.base
@brief Provides base types that should be used by all pgit commands

@author Sebastian Thiel
@copyright [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html)
"""
__all__ = ['CmdBase']

from mrv.cmd.base import SpawnedCommand

from git import Repo
import os

__all__ = ['CmdBase']

#{Classes

class CmdBase(SpawnedCommand):
	"""Implements functinality common to all pgit commands
	
	We initialize a member called 'repo' which provides a Repo instance based on 
	the current working directory"""

	def __init__(self, *args, **kwargs):
		super(CmdBase, self).__init__(*args, **kwargs)
		
		self.repo = Repo(os.getcwd())
	

#}END classes
