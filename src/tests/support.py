
import os, sys
sys.path.append(os.path.abspath('..'))

def test_findPreferences(manager):
    settings = manager.getPreferenceSettings('text.html.textile markup.heading.textile')
    for key in settings.KEYS:
        print key, getattr(settings, key, None)

def test_creationAndDeleteBundle(manager):
    bundle = manager.createBundle('Diego')
    bundle.save()
    item = manager.createBundleItem('MiSnippet', 'snippet', bundle)
    item.save()
    manager.deleteBundle(bundle)
    
if __name__ == "__main__":
    from prymatex.support.manager import PMXSupportManager
    manager = PMXSupportManager()
    manager.addNamespace('prymatex', os.path.abspath('../bundles/prymatex'))
    manager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
    manager.loadSupport()
    test_findPreferences(manager)