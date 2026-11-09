Python API reference
====================

The package exports :class:`mlx.Mlx`. Its methods are a thin wrapper over the
MinilibX C library documented in ``src/mlx.h``. Return codes from native
functions are passed through, typically as ``0`` on success. Calls that
produce a native pointer return ``None`` when creation fails.

.. currentmodule:: mlx

.. autoclass:: Mlx
   :members:

Callback signatures
-------------------

The callback aliases below are available from ``mlx.mlx`` and describe the
convenience hook methods:

* ``MouseCallback``: ``(button, x, y, param)``
* ``KeyCallback``: ``(keycode, param)``
* ``NoArgCallback``: ``(param,)``; used by expose and loop hooks
* ``HookCallback``: generic callback for :meth:`Mlx.mlx_hook`; its arguments
  depend on the event number

The generic hook uses raw X11 event numbers: key events 2 and 3 receive
``(keycode, param)``, button events 4 and 5 receive ``(button, x, y, param)``,
and motion event 6 receives ``(x, y, param)``. Other event numbers receive
``(param,)``. Event masks are backend dependent.

Image pixel data
----------------

``mlx_get_data_addr`` returns a writable view into the native image buffer.
Use ``size_line`` to find the start of each row; rows may include padding, so
do not assume the stride is ``width * bytes_per_pixel``. The returned
``format`` is ``0`` for B8G8R8A8 or ``1`` for A8R8G8B8. The view remains tied to
the native image and must not be used after ``mlx_destroy_image``.

For ``mlx_pixel_put`` and ``mlx_string_put``, the color is an unsigned integer.
On little-endian systems, the documented byte order corresponds to
``0xAARRGGBB``; the integer representation differs on big-endian systems.

Synchronization commands
-------------------------

Use :meth:`Mlx.mlx_sync` with one of the ``Mlx.SYNC_*`` constants:

* ``SYNC_IMAGE_WRITABLE`` (``1``): wait until an image can be written again.
* ``SYNC_WIN_FLUSH`` (``2``): wait until pending window requests are sent.
* ``SYNC_WIN_COMPLETED`` (``3``): wait until pending requests are sent and
  completed.

``mlx_do_sync`` flushes requests for all windows. On the AppKit backend, a
frame is shown only while ``mlx_loop`` pumps the native event loop; a sync call
alone does not display it.
