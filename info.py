# -*- coding: utf-8 -*-

#{ Configuration 
 
mrv_min_version = (1, 0, 1)		# ( major, minor, micro )
version = ( 0, 1, 0, 'beta', 0 )

project_name = "pgit"
root_package = "pgit"
author = "Sebastian Thiel"
author_email = 'byronimo@gmail.com'

url = 'https://github.com/Byron/pgit'
description = 'Git Commandline Tools written in Python'
license = "New BSD"

src_commit_sha = '0'*40

# paths to executables, relative to our project root
regression_test_exec = 'ext/mrv/test/bin/tmrvr'
nosetest_exec = 'ext/mrv/test/bin/tmrv'
makedoc_exec = '../ext/mrv/doc/makedoc'

setup_kwargs = dict(
				scripts = ['bin/pgit-submodule'], 
				package_data = {
								'pgit' : [ 'bin'],
								
								# MRV
								'pgit.ext.mrv' : ['bin', 'maya/cache'],
								'pgit.ext.mrv.test' : ['bin', 'cmd', '!*test_*'],
								
								 },
				requires=(	'GitPython (>=0.3.1)',
							'mrv (>=1.0.1)'),

				options = dict(build_py={	'exclude_from_compile' 	: ('*/maya/undo.py', '*/maya/nt/persistence.py'), 
										'exclude_items' 			: ( 
																		# MRV
																		'mrv.doc',
																		'mrv.test.maya.test_',
																		'mrv.test.maya.automation',
																		'mrv.test.maya.nt',
																		'mrv.test.maya.performance',
																		'mrv.test.maya.ui',
																		'mrv.test.fixtures', 
																		'mrv.test.automation',
																		'mrv.test.test_',
																		'mrv.test.cmd.test_',
																		
																	)} )
				)


# Optionally taken into consideration by the DocGenerator implementation 
doc_config = dict(
				epydoc_show_source = 'no',
				epydoc_modules = "modules: unittest\nmodules: ../",
				epydoc_exclude = "%s.test,%s.doc" % (root_package, root_package),
				)

#} END configuration
