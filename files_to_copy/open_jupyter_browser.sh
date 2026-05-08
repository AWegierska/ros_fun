#!/bin/sh

# Jupyter may generate a browser URL with 0.0.0.0 inside the container.
# That address is only a bind address, so open the usable local URL instead.
exec firefox http://localhost:8888/tree
