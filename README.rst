Prymatex Text Editor
--------------------

What is Prymatex
================

Pryamtex is a simple and flexible text editor. It's written in PyQt4 and
it's main aim is to support TextMate bundles.

Why Prymatex?
=============

There are thouthands of text editors out there, and many of them are
foused on writting code, just to name a few, Notepad++, Kate, Gedit,
Scribes, etc.

These editors are great, but the way they are way they're extended is
complex for non C/C++ programmers. That's where TextMate cames into place.
It allows to define syntaxes and tools in a very simple way plus there
are lots of these extensions (actually called Bundles) maintained by
enthuisasts. From Ruby on Rails, to OpenGL programming, these bundles come
with 3 basic components:

    * **Syntax** An extensible syntax format (allowing inclusion/usage, ie: PHP includes HTML and JS)

    * **Commands** They're like what we all know as marcros

    * **Snippets** Pieces of text that can be tirggered in certain situations

    * **Templates** File templates
    


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