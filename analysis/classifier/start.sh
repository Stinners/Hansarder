#! /usr/bin/env sh

uvicorn main:app --reload --reload-include *.css
