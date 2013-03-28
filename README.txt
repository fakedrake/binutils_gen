                                README
                                ======

Author: Chris Perivolaropoulos
Date: 2013-03-28 13:38:23 EET


Table of Contents
=================
1 Usage


1 Usage
========
  Here is how to use binutils_gen:
  - Clone this into NemaSpec
  - Make sure you have the =NEMA_ROOT= variable set to the root of
    the nema projects.
  - Then in NemaSpec create a virtual environment if you haven't done so already.



  cd $NEMA_ROOT/NemaSpec
  virtualenv --no-site-packages .


  - From the package's folder run setup.py install.



  cd binutils_gen
  ../bin/python setup.py install
  cd ..


  - Then run =bin/binutils_gen= from NemaSpec and everything will be
    done automagically

  - If you want to clean everything up, we support it now with the
    =-c= option.

  - To play with the command line parameters you can run

    bin/binutils_gen --help

  - To fiddle with opcode arguments' parsing you want to edit
    =binutils_gen/config.py=. The options in there should be more than
    enough.
