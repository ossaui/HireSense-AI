SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


def is_supported_resume(filename: str) -> bool:
    return any(filename.lower().endswith(extension) for extension in SUPPORTED_EXTENSIONS)
