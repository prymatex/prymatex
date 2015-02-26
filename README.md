# What is Prymatex

Prymatex is a simple and flexible text editor. It's written in PyQt and
it's main aim is to support TextMate bundles.

# Why Prymatex?

There are *enough* text editors out there, and many of them are
focused on writing code, just to name a few, Notepad++, Kate, Gedit,
Scribes, etc.

These editors are great, but the way they are way they are extended is
complex for non C/C++ programmers (although this is changing gradually).
That's where TextMate comes into place. It allows the user to define syntaxes, 
snippets, macros and commands in a very simple way, using 
shell scripting, Ruby, Python, PHP or any other tool wich can handle
shell variables and stdin/stdout pipes.

There are a lots of these extensions (actually called Bundles) maintained by
enthusiasts. From Ruby on Rails, to OpenGL programming, these bundles come
with some basic components like:

* **Syntax** An extensible syntax format (allowing inclusion/usage, ie: PHP includes HTML and JS)

* **Commands** They're like what we all know as marcros

* **Snippets** Pieces of text that can be tirggered in certain situations

* **Templates** File templates

# License

If not otherwise specified (see below), Prymatex code is distributed under the
terms of GPL V.2 licence, please refer to licenses/GPL2-license.txt.

An exception is made for files in readable text which contain their own license
information, or files where an accompanying file exists (in the “licenses“ directory)
with a “-license” suffix added to the base-name name of the original file, and an
extension of txt, html, or similar. For example “pyqt” is accompanied by
“pyqt-license.txt”.

# Running Prymatex

See INSTALL.md to setup your enviroment.