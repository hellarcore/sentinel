#!/bin/bash
set -evx

mkdir ~/.hellar

# safety check
if [ ! -f ~/.hellar/.hellar.conf ]; then
  cp share/hellar.conf.example ~/.hellar/hellar.conf
fi
