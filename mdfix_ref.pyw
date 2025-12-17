from mdfix.runner import get_argv_paths, normalize_md

if __name__ == "__main__":
    normalize_md(paths=get_argv_paths(), mode="normalize_refs")
