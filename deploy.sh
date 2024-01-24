sudo python3 setup.py sdist
suffix=".tar.gz"
PACKAGE=`ls ./dist | grep ${suffix}`
mkdir ./tmp
cp "./dist/$PACKAGE" ./tmp
cd ./tmp
tar -xvzf $PACKAGE
cd ${PACKAGE%"$suffix"}
sudo python3 setup.py install
# clean up
cd ../..
sudo rm -r ./tmp
sudo rm ./dist/*
