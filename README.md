# `tab` is for processing tabular data

`tab` extracts and reformats tabular data in the command line, notably by picking
out selected columns.

Lots of programs produce tabular output; `cut` gives you one column or a range
of columns, but only accepts a 1-byte delimiter so space aligned stuff wont
work, Unicode separators won’t work, etc.

Awk has a much better field-splitting algorithm which accepts either tabs or ≥2
spaces as a field separator, so i end up doing this a lot:

    some_program | awk '{print $2}'

which is silly, long, and inflexible (note you have to use single quotes cause
double quotes interpolate on `$`!).

I started work on `tab` a while back but seem to have lost the source code.

## Goals
* Awk’s splitting algorithm
* Specifying lists of ranges should be really easy by-default
