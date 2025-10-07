from setup.tickerSetup import get_mapping
from setup.sicSetup import getSector

def masterSetup():
    get_mapping()
    getSector()
    
if __name__ == '__main__':
    masterSetup()