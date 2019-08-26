import pytest
from werkzeug.security import safe_str_cmp
from appium import webdriver
from timeit import default_timer as timer
from datetime import timedelta
from config.evidence_gen import EvidenceGenerator
from werkzeug.security import safe_str_cmp

SCREENSHOT = 'screenshots/'


def pytest_sessionstart(session):
    session.results = dict()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.session.results[item] = result

def pytest_sessionfinish(session, exitstatus):
    return sum(1 for result in session.results.values() if result.failed)

@pytest.yield_fixture(scope='function')
def Device(request, device):
    print("Running device setUp")
    if safe_str_cmp(device,'ios'):
        print("Tests will be executed on ios")
        driver = webdriver.Firefox()
    elif safe_str_cmp(device,'android'):
        print("Tests will be executed on Android")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.1'
        desired_caps['automationName'] = 'uiautomator2'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = '../../../apps/selendroid-test-app.apk'

        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    
    #add implicity wait

    if request.cls:
        request.cls.driver = driver
    
    yield driver

def pytest_addoption(parser):
    parser.addoption("--device")
    parser.addoption("--osType", help="Operating system...")

@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--device")

@pytest.fixture(scope='session')
def osType(request):
    return request.config.getoption("--osType")

@pytest.fixture(scope='session')
def GenerateEvidence(request,scope='session'):
    pytest.time_start = timer()
    session=request.node
    yield
    result = "Failed" if sum(1 for result in session.results.values() if result.failed) > 0 else "Passed"
    import os
    pytest.time_end = timer()
    doc = EvidenceGenerator("Mobile Test Automation Framework", 
                            str(round(pytest.time_end - pytest.time_start,2)) , result)
    TEST_DIR = SCREENSHOT+str(pytest.time_start)
    dirs = os.listdir(TEST_DIR)  
    for subdir in dirs:
        evidencias = []
        evidencias = os.listdir(TEST_DIR+'/'+subdir+'/')
        for e in evidencias:            
            doc.addEvidence(subdir,e,TEST_DIR+'/'+subdir+'/'+e)
    doc.createDocument(TEST_DIR+'/'+"doc.docx")
