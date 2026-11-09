MinilibX Python API
===================

MinilibX is a small graphics library for creating windows, drawing pixels and
images, and handling basic input. The ``mlx`` Python package provides a thin
``ctypes`` wrapper around the native library.

These pages describe the Python interface. The wrapper follows the C API names
from ``mlx.h`` while adapting pointer output arguments to Python return values.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started
   api

Quick example
-------------

This example opens a window, draws a pixel, and exits the event loop when a key
is released:

.. code-block:: python

   from mlx import Mlx

   mlx = Mlx()
   mlx_ptr = mlx.mlx_init()
   if mlx_ptr is None:
       raise RuntimeError("Could not connect to the display")

   win_ptr = mlx.mlx_new_window(mlx_ptr, 320, 200, "MinilibX")
   if win_ptr is None:
       mlx.mlx_release(mlx_ptr)
       raise RuntimeError("Could not create a window")

   # On little-endian systems, colors use the integer form 0xAARRGGBB.
   mlx.mlx_pixel_put(mlx_ptr, win_ptr, 160, 100, 0xFFFF0000)

   def stop_on_key_release(keycode, _state):
       mlx.mlx_loop_exit(mlx_ptr)

   mlx.mlx_key_hook(win_ptr, stop_on_key_release, None)
   mlx.mlx_loop(mlx_ptr)

   mlx.mlx_destroy_window(mlx_ptr, win_ptr)
   mlx.mlx_release(mlx_ptr)

The key hook runs when a key is released. Its ``keycode`` is backend and
keyboard-layout dependent; this example exits on any key release.

.. note::

   ``Mlx()`` loads the native shared library shipped with the Python package.
   Build and install the package for your platform before creating an ``Mlx``
   instance. See :doc:`getting_started`.
