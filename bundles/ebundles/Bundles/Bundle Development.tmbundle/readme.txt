== Bundle Development port for E Text Editor
This is a port of the Bundle Development bundle:
http://snipr.com/bundle_development

== Maintainer(s)
Charles Roper
reachme [at] charlesroper [dot] co [dot] uk

== Notes
29/02/2008
The following changes were made:

  "Help%3A Scope Conventions.tmCommand" now opens the Macromates site in an external browser.

  Scope Completion was removed due to it using the ui library

  Show Changes was removed due to unavailability of pl command (anyone know what this is?)

  "ENV['TM_%E2%80%A6'].tmSnippet" was changed because of incompatibilities with E snippet engine

  "Require 'Support%3Alib%3A%E2%80%A6'.tmSnippet" was changed because of incompatibilities with E snippet engine

16/03/2008 andrey.turkin
Update from tmbundles4win, almost verbatim except for:

  "Help: Scope Conventions" was fixed to work with IE too

  pl and plutil commands were put in support/bin (pl doesn't work as MacOS version but should suffice for "Show Changes" command