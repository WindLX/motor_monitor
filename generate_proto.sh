#!/bin/bash

SRC_DIR=./proto
DST_DIR=./generated

protoc --proto_path="$SRC_DIR" \
    --python_out="$DST_DIR" \
    --pyi_out="$DST_DIR" \
    "$SRC_DIR/bit.proto"