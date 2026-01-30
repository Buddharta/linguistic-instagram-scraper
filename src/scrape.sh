#!/bin/sh
USERS=("vickywolff" "juliolealortiz" "edificiosmayas" "santos_tuz" "elsocotroco" "lasmacucasoficial" "tilasesto" "chuchopitza" "eljuanamaro")

instaloader --no-compress-json --comments +args.txt --profile "${USERS[@]}"

