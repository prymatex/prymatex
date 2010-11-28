## Notice

This is a TextMate compatible bundle for using the [Sass](http://sass-lang.com/) CSS enhancement language by Hampton Catlin, Nathan Weizenbaum and Chris Eppstien.

This bundle was originally written in order to provide Sass snippets, but since then there have been many fantastic contributions. Thanks to Github for making it easy to bring all of those contributions together:

* [@agibralter](http://github.com/agibralter)
* [@aussiegeek](http://github.com/aussiegeek)
* [@charlesr](http://github.com/charlesr)
* [@choan](http://github.com/choan)
* [@giannichiappetta](http://github.com/giannichiappetta)
* [@gruner](http://github.com/gruner)
* [@mattpolito](http://github.com/mattpolito)
* [@mattsa](http://github.com/mattsa)
* [@mfilej](http://github.com/mfilej)
* [@squishtech](http://github.com/squishtech)
* [@tharealpatton](http://github.com/tharealpatton)
* [@trevorsmith](http://github.com/trevorsmith)

## Installation

### Textmate (OS X)

#### With Git:

    mkdir -p ~/Library/Application\ Support/TextMate/Bundles
    cd ~/Library/Application\ Support/TextMate/Bundles
    git clone git://github.com/charlesr/ruby-sass-tmbundle.git "Ruby Sass.tmbundle"
    osascript -e 'tell app "TextMate" to reload bundles'

#### Without Git:

    mkdir -p ~/Library/Application\ Support/TextMate/Bundles
    cd ~/Library/Application\ Support/TextMate/Bundles
    wget http://github.com/charlesr/ruby-sass-tmbundle/tarball/master
    tar zxf aussiegeek-ruby-sass-tmbundle*.tar.gz
    rm aussiegeek-ruby-sass-tmbundle*.tar.gz
    mv aussiegeek-ruby-sass-tmbundle* "Ruby on Rails.tmbundle"
    osascript -e 'tell app "TextMate" to reload bundles'

### E Text Editor (Windows)

A reasonably up-to-date version of this bundle is usually available for installation via the Bundles Manager (*Bundles > Edit Bundles > Manage Bundles*). Unless you want the bleeding edge version of this bundle, install from there. Otherwise:
    
#### With msysGit:
  
Make sure msysGit is installed, then at the command line:
    
    cd %appdata%\e\Bundles
    git clone git://github.com/charlesr/ruby-sass-tmbundle.git "Ruby Sass.tmbundle"

In E, select *Bundles > Edit Bundles > Reload Bundles*
    
#### Without msysGit:

Download the bundle using Github's "Download" button and extract the content of the folder contained in the zip file into:

    %appdata%\e\Bundles\Ruby Sass.tmbundle\
