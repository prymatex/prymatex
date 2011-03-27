Using Prymatex
==============


Supported Platforms
-------------------

Despite having started as a cross platform project, we are currently focusing development
on Linux plaform. We're testing it on Ubuntu 10.10 and Gentoo Linux.



Requirements
------------

Running (using prymatex). 

	* Linux
		
		

	* PyQt4
	
	* ponyguruma
	
		Install it from Git with the folowing commands
		
		.. code-block:: bash
		
			cd ~ # Move to you local folder
			mkdir tmp
			cd tmp
			git clone https://github.com/D3f0/ponyguruma.git
			cd ponyguruma
			su -c "python setup.py install" # or sudo python setup.py install on Ubuntu 
	
	* **Bundles**
	
Development (improving prymatex or creating new bunldes)
--------------------------------------------------------

All the previous sections plus
	
	* GNU Make
	
		You probably have this tool already in you system, just type ``make``
		and you should see something link this::
		
			make: *** No targets specified and no makefile found.  Stop.
		
		Otherwise install it with::
		
			sudo apt-get install make

	* PyQt4 develompent tools
	
		.. code-block:: bash
		
			sudo apt-get install pyqt4-dev-tools