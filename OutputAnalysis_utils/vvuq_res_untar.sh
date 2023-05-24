#!/bin/bash

target="fhivib.tar.gz"
file_path="dir_tmp.txt"

ls | grep "run_" > $file_path

while IFS= read -r line; do
	cd $line
		tar -xvf $target
	cd ..
done < "$file_path"
