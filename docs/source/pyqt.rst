PyQt and Prymatex
=================


Working with the GUI layout
---------------------------

Most Prymatex widget layouts, such as the main window,
code editor, file pane, project pane, etc. are designed 
with Qt's Designer tool [*]_. This tool produces language
agnostic XML files. These files usually have a **ui** file
estension, and are generally compiled through **pyuic** tool
to obtain python code for you layout.

This is a code snippet compiles a **ui** file into a python
code, although not essential the **-x** definitions adds a 
main function that might by useful to check how the layout
looks like without opening Designer.

.. code-block:: bash

	pyuic -x my_nice_layout.ui -o my_nice_layout.py


Desinger File Organization
--------------------------

We've standariezed where to put thse **ui** files and automated


Defining and Using Custom widgets
---------------------------------


.. [*] http://doc.qt.nokia.com/latest/designer-manual.html

