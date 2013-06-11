======================================================
Installing Prymatex
======================================================

Getting the code
~~~~~~~~~~~~~~~~

Grab the code from github typing the following line in
you terminal::

	git clone https://github.com/prymatex/prymatex
	
Prymatex comes with a set of bundles taken from TextMate's
repo::
	
	http://svn.textmate.org/trunk/
	
Windows user won't be able to run prymatex outside 
a cygwin environment because of filesystem character
restrictions. Stay tunned we will fix it soon.

Prerequisites
~~~~~~~~~~~~~

In order to install Prymatex you need to make sure you have:

	* PyQt4
	* pyzmq
	* ponyguruma
	* xmodmap

Additionally you should install pip requirements::

	pip install -r requirements.txt 
	
Running Prymatex
~~~~~~~~~~~~~~~~

To run prymatex, simply type::

	pmx.py
	
Finally, if you like to run it from anywhere, add it 
to your path::

	echo "export PATH=$PATH:/path/to/prymatex/bin" >> ~/.bashrc
	
or ``.zshrc``/``.zshrc.${USER}`` if you're using zsh/oh-my-zsh