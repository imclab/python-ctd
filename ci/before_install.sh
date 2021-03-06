# http://stackoverflow.com/questions/17224389/
# scipy-importerror-on-travis-ci

# Install Dependencies.
SITE_PKG_DIR=$VIRTUAL_ENV/lib/python$TRAVIS_PYTHON_VERSION/site-packages
echo "Using SITE_PKG_DIR: $SITE_PKG_DIR"

# Workaround for travis ignoring system_site_packages in travis.yml.
rm -f $VIRTUAL_ENV/lib/python$TRAVIS_PYTHON_VERSION/no-global-site-packages.txt

sudo apt-get update -qq
sudo apt-get install -qq build-essential
sudo apt-get build-dep -qq python-scipy
sudo apt-get build-dep -qq python-numpy
sudo apt-get build-dep -qq python-pandas
