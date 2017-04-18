
from .naming import get_dir_name_v1
from .io import create_dir_if_not_exists_recursively


def prepare_dir(vendor, date, page_type='common'):
    dir_name = get_dir_name_v1(vendor, date, page_type)
    create_dir_if_not_exists_recursively(dir_name)
    return dir_name
