import sys

def main():
    if (len(sys.argv) > 1):
        print(f'{sys.argv}')
        if ('sim' in sys.argv):
            from hexl.core.Simulator import Simulator
            app = Simulator()
    else:
        from hexl.core.TopLevel import Hexl
        app = Hexl()
    
    app.run()

if __name__ == '__main__':
    main()
