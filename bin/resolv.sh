#!/bin/bash

sudo repoquery -R --resolve --recursive "$1" --qf="%{name}" 2>/dev/null


