from uuid import UUID


def convert_string_to_uuid(s: str):
    try:
        return UUID(s)
    except ValueError:
        return None
