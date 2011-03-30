Intoruction to Prymatex
=======================


Why Pryamtex?
-------------

Prymatex is a general purpouse text editor baed in Mac's TextMate_ application.
Oringinally called Crossmates [*]_ , we decided to change its name after serious 
development took off.


Prymatex main goal is to support TextMate's bundles [*]_, these bundles provide
syntax definition, code snippets, file templates and commands, among 
other things. There are a lot of bundles out there, 
most of them maintained by TextMate community.

There are some TextMate clones already, such as eTextEditor and InType, that bring
TextMate's magic into Microsoft Windows world, although they can be used under Linux
with wine, emulation is not an option for serious development and Prymatex authors
main operating system is Linux :P.




.. [*] Read on about TextMate bundles and how we implement them in TodoInserBundleSction

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

.. 
	UML idea from
	http://www.ffnn.nl/pages/articles/media/uml-diagrams-using-graphviz-dot.php


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
		"app" [label = "{PMXApplication|settings}"];
		"file manager" [label = "{PMXFileManager\
		|opened_files = \{\}}"];
		
		"file" [label = "{PMXFile|\
			path|\
			save()\n\
			read()\n\
			write()\n\
			fileSaved(QString) [singal] \n\
	    	fileRenamed(QString)[signal]\n\
	    	fileSaveError(QString) [signal]\n\
	    	fileLostReference() [signal]\n\
			}" ];
		
		"window" [label = "{PMXMainWindow|tabWidget}" ];
		"tab widget" [label = "{PMXTabWidget|}"];
		"editor widget" [label = "{PMXEditorWidget|editorFactory(cls...)\
		\nregisterEditor(cls,...)|}"];
		
		"code edit" [ label = "{PMXCodeEdit|\
			syntax|\
			}" ];
		
		
		subgraph clusterAnimalImpl {
			label = "prymatex.bundles"
			
			"bundle" [label = "{PMXBundle||}"]
			"syntax" [label = "{PMXSyntax||}"]
		
		}
		
		
		"syntax" -> "bundle" [headlabel="1..n" taillabel=""]
		
		
		
		// Arrows
		"file" -> "file manager" [label = "parent"];
		"app" -> "window" [label = "holds"];
		"app" -> "file manager";
		"editor widget" -> "tab widget" [label = "parent"];
		"editor widget" -> "file" [label = "file"];
		"tab widget" -> "window" [label = "parent" ];
		"code edit" -> "editor widget" [label = "parent" ];
		
		"code edit" -> "syntax" [label = "syntax"];
		
		
	}
	

.. inheritance-diagram:: prymatex.core.app.PMXApplication



