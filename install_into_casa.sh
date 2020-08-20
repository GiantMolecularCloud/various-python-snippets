####################################################################################################
# INSTALL PACKAGES TO CASA
####################################################################################################
#
# This is only vaguely a python snippet but it helps to work with CASA which has a python interface.
# CASA (https://casa.nrao.edu/) is built on a heavily outdated python kernel and lacks many useful
# packages. It is however possible to install many python packages right into CASA. This is described
# here: https://casaguides.nrao.edu/index.php/OtherPackages
# The install routine requires to start CASA twice which can be annoying. This script will install
# the given PACKAGES automatically.

####################################################################################################
# packages to be installed
####################################################################################################

# Not all python packages work. Just try it and if using the package fails, the installation will
# only caused CASA to take up a few bytes more storage but not cause harm.

PACKAGES=(astropy aplpy=1.1.1)


####################################################################################################
# install pip into CASA
####################################################################################################

casa --nologger --log2term <<-casaINPUT
    from setuptools.command import easy_install
    easy_install.main(['--user', 'pip'])
casaINPUT


####################################################################################################
# install the packages
####################################################################################################

FormattedPackageList="["
for i in "${PACKAGES[@]}"
do
    FormattedPackageList=$FormattedPackageList"'$i', "
done
FormattedPackageList=${FormattedPackageList::-2}"]"

casa --nologger --log2term <<-casaINPUT
    import pip
    for package in $FormattedPackageList: pip.main(['install', package, '--user'])
casaINPUT


####################################################################################################
#
####################################################################################################
