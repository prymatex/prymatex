STYLE = """
<style type='text/css'>
    *{margin:0px;}
    .oculto{ display:none;}
    .recuadro{ border:1px dotted #cccccc; margin:10px;padding:10px;}
    .bundle_box{ margin:10px; padding:0px;}
    .bundle_box h3 { color: #555555; margin:0px; padding:2px;cursor:pointer; border:1px solid #cccccc; }  
    .bundle_box h3:hover{ color: #FFFFFF; margin:0px; padding:2px; background: -webkit-gradient(linear, left top, left bottom, from(#4674CB), to(#1F3B6F));cursor:pointer;}  
    h3.seleccionado{ color: #FFFFFF; margin:0px; padding:2px; background: -webkit-gradient(linear, left top, left bottom, from(#4674CB), to(#1F3B6F));cursor:pointer;}  
    table{ margin:10px; border: 1px solid #cccccc;padding:0px;}
    table th{background-color: #cccccc; color: #555555; padding:5px; width:50%;}
    table td{ border:1px solid #cccccc;text-align:left; padding-left:10px;}
    table tr:hover{ background-color: #cccccc; }
    #logo{ color: #555555; font-size:1.5em; -webkit-transition: all 1s ease-in-out;  text-align:center;  }
    #logo:hover{ 
        -webkit-transform: rotate(10deg) scale(4);
        color: #FFFFFF; margin:0px; padding:2px; background: -webkit-gradient(linear, left top, left bottom, from(#4674CB), to(#1F3B6F));
        margin-top:60px;
    }
</style>
"""

THE_JS = """
<script type='text/javascript'>
  
    function toggle(ele,uuid){
      
        box = document.getElementById(uuid);
      
        if (ele.className == ''){
           ele.className = 'seleccionado';
        }else{
           ele.className = '';
        }
        
        if (box.className == 'oculto'){
            box.className='';
        }else{
            box.className='oculto';    
        }
        
        return false;
    }
    
</script>
"""

import sys
import os


try:
    TM_APP_PATH = os.environ['TM_APP_PATH']
    TM_BUNDLES_PATH = os.environ['TM_BUNDLES_PATH']
except Exception, e:
    TM_APP_PATH = "../../"



sys.path.append(os.path.abspath(os.path.join(TM_APP_PATH , '..')))

from prymatex.bundles import BUNDLEITEM_CLASSES
from prymatex.bundles import load_prymatex_bundles
from prymatex.bundles.base import *
from glob import glob

if __name__ == "__main__":
    
    bundles_to_show = '*.tmbundle'
    
    if(len(sys.argv) > 1):
        bundle_to_show = sys.argv[1]
        bundles_to_show = '*%s*.tmbundle' % bundle_to_show

    print STYLE
    print "<div class='oculto'>"
    
    for file in glob(os.path.join(TM_BUNDLES_PATH, bundles_to_show)):
        PMXBundle.loadBundle(file, BUNDLEITEM_CLASSES)

    print "</div>"
    
    
    
    print "<div id='logo'>Prymatex Bundles</div>"
    
    for uuid in PMXBundle.BUNDLES:
        
        print "<div class='bundle_box'>"
        
        bundle = PMXBundle.BUNDLES[uuid]
        
        print "<h3 onclick=toggle(this,'%s')>%s</h3>" % (uuid, bundle.name)
        
        print "<div class='oculto' id='%s'>" % uuid
        
        
        try:
            print "<div class='recuadro'>%s</div>" % unicode(bundle.description)
        except UnicodeEncodeError, e:
            print "<div class='recuadro'>No puedo mostrar la descripci&oacute; por problemas con caracteres extra&ntilde;os</div>"
        
        if bundle.snippets:
            print "<div class='recuadro'>"
            print "<h4>Snippets:</h4>"
            print "<table>"
            print "<thead><th>Name</th><th>tabTrigger</th><th>keyEquivalent</th></thead>"
            for snippet in bundle.snippets:
                try:
                    print "<tr><td>%s</td><td>%s</td><td>%s</td>" % (snippet.name, snippet.tabTrigger, snippet.keyEquivalent)
                except:
                    pass
            print "</table>"
            print "</div>"
        
        if bundle.snippets:
            print "<div class='recuadro'>"
            print "<h4>Commands:</h4>"
            print "<table>"
            print "<thead><th>Name</th><th>tabTrigger</th><th>keyEquivalent</th></thead>"
            for command in bundle.commands:
                try:
                    print "<tr><td>%s</td><td>%s</td><td>%s</td>" % (command.name, command.tabTrigger, command.keyEquivalent)
                except:
                    pass
            print "</table>"
            print "</div>"
        
        print "</div>"
        print "</div>"
    
    print "<br>code is poetry..."
        
    print THE_JS
