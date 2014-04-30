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
regression_test_exec = 'pgit/ext/mrv/mrv/test/bin/tmrvr'
nosetest_exec = 'pgit/ext/mrv/mrv/test/bin/tmrv'
makedoc_exec = '../pgit/ext/mrv/doc/makedoc'

setup_kwargs = dict(
				scripts = ['pgit/bin/pgit-submodule'], 
				package_data = {
								'pgit' : ['bin/*'],
								 },
				requires=('gitpython (>=0.3.1)',),
				install_requires='gitpython >= 0.3.1',
				options = dict()
				)


# Optionally taken into consideration by the DocGenerator implementation 
doc_config = dict(
				epydoc_show_source = 'no',
				epydoc_modules = "modules: unittest\nmodules: ../pgit",
				epydoc_exclude = "%s.test" % (root_package),
				)

#} END configuration
