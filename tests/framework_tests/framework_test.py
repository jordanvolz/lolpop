from lolpop.base_integration import BaseIntegration
from pathlib import Path 

parent_dir = Path(__file__).parent.resolve()
framework_files = "%s/framework_files" % parent_dir

def test_default_framework(): 
    int = BaseIntegration()
    assert int.integration_framework.height == 2
    assert int.integration_framework.size == 4
    assert int.integration_framework.is_root
    children = [x.id for x in int.integration_framework.children]
    assert "component" in children
    assert "pipeline" in children
 

def test_custom_framework(): 
    int = BaseIntegration(conf="%s/framework.yaml" %framework_files)
    assert int.integration_framework.height == 3
    assert int.integration_framework.size == 7
    assert int.integration_framework.is_root
    children = [x.id for x in int.integration_framework.children]
    assert "component" in children
    assert "pipeline" in children
    assert "widget" in children

def test_multiple_root_nodes_fails(): 
    try: 
        int = BaseIntegration(conf="%s/framework_fails.yaml" %framework_files)
    except Exception as e: 
       assert "ERROR: Detected more than one root node in integration framework." in str(e)

def test_standlone_integration():
    int = BaseIntegration(is_standalone=True)
    assert int.integration_framework is None