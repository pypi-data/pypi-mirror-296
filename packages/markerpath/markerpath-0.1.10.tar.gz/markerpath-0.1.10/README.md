Usage:

1. Create a file with extension .marker in your base directory.  
2. Contents of this file
    Nothing
    OR
    lines of path relative to the base directory that contains python executable. These paths will be appended 
    by the import to the sys.path
3. In your python file with main anywhere under the base directory.
    import markerpath

    3.1 This will create a environment variable 
        MARKER_PATH=<the base directory>

    3.2 Access this as such
        import os
        marker_home=os.environ["MARKER_PATH"]


