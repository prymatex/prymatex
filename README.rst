Prymatex Text Editor
--------------------

What is Prymatex
================

Pryamtex is a simple and flexible text editor. Even though it's meant for
programmers (since its primary goal is to be useful for its authors), we
belive it might be helpful for those who whant a snappy GUI which wraps 
Unix utilites. 

Why Prymatex?
=============

Most modern IDE eat a lot of RAM. Most modern GUIs are quite powerful, take
Eclipse or NetBeans for instance.

Python is a singular language, it's fun and it can be used for simple automation
tasks and for big system architectures, with lots of layers and high complexity.


Main Objectives
===============

Prymatex main objectives are:

* Syntax highlighting and formating (take as much of TextMate as possible,
  it has a lot of syntax definitions)
* Snippets
* Commands
* Plugins (these things extend the UI in some way)
    
* Debugging
*
* (D)CVS integration
* Git
* Mercurial
* Bazaar
* Any other tool
    
    * Spell checking (based on aspell/ispell)
    
    

How to run prymatex
===================

The requirements to run pryamtex are:

* Python 2.6
* PyQt4 >= 4.5
* Oniguruma (this library may be bundled with this app)
    
Additional libraries may be needed for specific plugins. Most TextMate bundles
should as long as you fulfill its requirements (i.e. php cli for php, or make
binary for C projects, and so on).