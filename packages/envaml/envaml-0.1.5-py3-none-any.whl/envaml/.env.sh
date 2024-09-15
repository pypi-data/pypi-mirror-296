#!/bin/bash

output_file="variables.txt"


for key in "${!vars[@]}"; do
    echo "$key=\"${vars[$key]}\"" >> $output_file
done