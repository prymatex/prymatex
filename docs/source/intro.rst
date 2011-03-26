Intoruction to Prymatex
=======================


Why Pryamtex?
-------------

Prymatex is a general purpouse text editor baed in Mac's TextMate_ application.
Oringinally called Crossmates [*]_ , we decided to change its name after serious 
development took off.



.. _TextMate: http://macromates.com

.. [*] Corssmates repositories are still available at `Google Code`_ and `Bit Bucket`_. 

.. _Google Code: http://code.google.com/p/crossmates/

.. _Bit Bucket: https://bitbucket.org/D3f0/crossmates/overview


A little bit of history about Prymatex
--------------------------------------






Prymatex Architecture Overview
------------------------------

This diagram show Prymatex architecture

.. graphviz::

	digraph foo {
		graph [
			rankdir = "LR"
		];
		node [ shape = "record" ];
		"app" [label = "PMXApplication|settings"];
		"file manager" [label = "PMXFileManager|opened_files = \{\}"];
		"file" [label = "PMXFile" ];
		"window" [label = "PMXMainWindow|" ];
		"tab widget" [label = "PMXTabWidget"];
		"editor widget" [label = "PMXEditorWidget"];
		"file" -> "file manager" [label = "parent"];
		"app" -> "window" [label = "holds"];
		"app" -> "file manager";
		"editor widget" -> "tab widget" [label = "parent"];
		"editor widget" -> "file" [label = "file"];
		
		
		
		
	}