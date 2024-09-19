======
seqpad
======

Overview
--------

Pad nucleotide sequence.

Installation
------------

To install ``seqpad``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install seqpad

Features
--------

The core function of this project is implemented as follows:

.. code-block:: python

    def seqpad(seq):
        while len(seq) % 3 != 0:
            seq += "N"
        return seq

The project also provides a CLI that can also be accessed from within python. For more information read the help message that can be accessed through one of the two following ways.

.. code-block:: bash

    # bash
    python3 -m seqpad -h

.. code-block:: python

    # python
    import seqpad
    seqpad.main(['-h'])

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/seqpad>`_
* `Download <https://pypi.org/project/seqpad/#files>`_
* `Source <https://github.com/johannes-programming/seqpad>`_

Credits
-------

* Author: Johannes
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``seqpad``!