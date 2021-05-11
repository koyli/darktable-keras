# darktable-keras

This is a simple project that uses deep learning categorization to
add tags to photos in Darktable.

The default is to use ResNet50, pretrained with the Imagenet data set.
YMMV.

Usage:

- python label-images.py {directory}

This will 
- recursively find ".xmp" files (sidecar files)
- classify the image according to the top 3 matches found by applying the trained network to the corresponding image
- add tags (keras|class_1) for each of the 3 top classes to the tags in the XMP files

Darktable does not normally read its XMP files, it uses its own database file at startup.  It does update the XMP files when the picture is edited (eg. a 1-way sync).  To enable Darktable to read the new XMP, in Darktable's Settings / Storage / XMP set "look for updated XMP files on startup" and set this to on - and restart Darktable to read any changes.

It appears that sometimes any new tag categories added may not be visible on first load, thus a second restart of Darktable may be necessary after any classification run.
