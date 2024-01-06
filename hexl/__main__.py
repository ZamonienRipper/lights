import sys

def main():
    if (sys.argv[1] == 'sim'):
        from hexl.core.Simulator import Simulator
        app = Simulator()
    else:
        from hexl.core.TopLevel import Hexl
        app = Hexl()
    
    app.run()

if __name__ == '__main__':
    main()
