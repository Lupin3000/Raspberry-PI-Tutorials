#!/usr/bin/env bash

function write_to_dev {
  echo -ne "$1" > /dev/hidg0
}

# Fuck (String)
write_to_dev "\x20\0\x9\0\0\0\0\0"
write_to_dev "\0\0\x18\0\0\0\0\0"
write_to_dev "\0\0\x6\0\0\0\0\0"
write_to_dev "\0\0\xe\0\0\0\0\0"

# [SPACE]
write_to_dev "\0\0\x2c\0\0\0\0\0"

# you (String)
write_to_dev "\0\0\x1d\0\0\0\0\0"
write_to_dev "\0\0\x12\0\0\0\0\0"
write_to_dev "\0\0\x18\0\0\0\0\0"

# [ENTER]
write_to_dev "\0\0\x58\0\0\0\0\0"

# Release al keys
write_to_dev "\0\0\0\0\0\0\0\0"

exit 0