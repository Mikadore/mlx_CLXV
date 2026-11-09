Getting started
===============

Install the Python package
--------------------------

The native library must be built for the platform where the program will run.
From the repository root, select a backend and build the project:

.. code-block:: console

   $ ./configure.sh
   $ make

On Linux, the default backend is XCB. You can select Wayland with
``make BACKEND=wayland``. On macOS, use ``make BACKEND=appkit``. The build
script checks the required system packages and tools; see the repository
root ``README.md`` for backend dependencies and configuration details.

The build creates a wheel in the repository root. Install the generated wheel
inside the virtual environment for your application:

.. code-block:: console

   $ python -m pip install ./mlx-*-py3-none-any.whl

Then import and initialize the wrapper:

.. code-block:: python

   from mlx import Mlx

   mlx = Mlx()
   mlx_ptr = mlx.mlx_init()
   if mlx_ptr is None:
       raise RuntimeError("Could not connect to the display")

``mlx_init`` must succeed before creating windows or images. ``Mlx()`` loads
the shared library from beside the installed Python module, so the wheel and
the native library need to come from the same build.

Build these docs
----------------

Install the documentation dependencies and build the HTML site:

.. code-block:: console

   $ python -m pip install -r docs/requirements.txt
   $ sphinx-build -b html docs docs/_build/html

The HTML entry point is ``docs/_build/html/index.html``. Read the Docs uses
the same Sphinx configuration and the Read the Docs theme.

Python wrapper behavior
-----------------------

The wrapper keeps the native function names and generally the same argument
order as the C API. Native pointers are represented as integer-like handles;
pass them back to MLX methods and do not inspect or modify them. Methods that
create a connection, window, or image return ``None`` on failure.

Several C functions fill output pointers. Their Python equivalents return the
outputs directly:

* ``mlx_get_data_addr(img_ptr)`` returns ``(pixels, bits_per_pixel,
  size_line, format)``. ``pixels`` is a writable ``memoryview``.
* ``mlx_mouse_get_pos(win_ptr)`` returns ``(status, x, y)``.
* ``mlx_get_screen_size(mlx_ptr)`` returns ``(status, width, height)``.
* ``mlx_xpm_file_to_image`` and ``mlx_png_file_to_image`` return
  ``(image, width, height)``.

Hook methods accept Python callables and an arbitrary ``param`` object. The
wrapper retains references to registered callbacks and parameters for as long
as they are registered. Pass ``callback=None`` to clear a hook.
