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


TODO

Prymatex Architecture Overview
------------------------------

This diagram show Prymatex architecture

.. graphviz::

	digraph G {
		
		fontname = "Bitstream Vera Sans"
        fontsize = 8

        node [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
                shape = "record"
        ]

        edge [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
        ]
		node [ shape = "record" ];
		// Nodes
		"app" [label = "PMXApplication|settings"];
		"file manager" [label = "PMXFileManager\nopened_files = \{\}"];
		"file" [label = "PMXFile\nsave()\nread()\nwrite()\n" ];
		"window" [label = "PMXMainWindow\n" ];
		"tab widget" [label = "PMXTabWidget"];
		"editor widget" [label = "PMXEditorWidget\neditorFactory(cls...)\
		\nregisterEditor(cls,...)"];
		"code edit" [ label = "PMXCodeEdit" ];
		
		// Arrows
		"file" -> "file manager" [label = "parent"];
		"app" -> "window" [label = "holds"];
		"app" -> "file manager";
		"editor widget" -> "tab widget" [label = "parent"];
		"editor widget" -> "file" [label = "file"];
		"tab widget" -> "window" [label = "parent" ];
		"code edit" -> "editor widget" [label = "parent" ];
		
		
	}
	
	
.. inheritance-diagram:: prymatex.core.app.PMXApplication



