from terminology.vsac import VSAC

def test_vsac():
    vsac = VSAC()
    valuesets = vsac.get_valuesets()
    print(valuesets)

if __name__ == "__main__":
    test_vsac()