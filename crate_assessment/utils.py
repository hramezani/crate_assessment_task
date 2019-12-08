def get_files_list(path):
    """
    Generator to list files in a directory.
    """
    for item in path.iterdir():
        if not item.is_dir():
            yield item
