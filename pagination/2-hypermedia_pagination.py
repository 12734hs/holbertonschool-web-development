#!/usr/bin/env python3
"""
    We use that function for creating pagination main variables
    start we use for found out when the data starts
    end for find out when we have to stop show our data
"""
import csv
import math
from typing import List, Dict, Union


def index_range(page=1, page_size=10):
    """
    We use that function for creating pagination main variables
    start we use for found out when the data starts
    end for find out when we have to stop show our data
    """
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """INit file, if you dunno"""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        So, this is the method for getting the pages of data, and here
        we are going to use the index_range function, which was
        implemented in the previous task
        """
        data = self.dataset()
        assert isinstance(page, int) and page > 0, "Cant be the 0"
        assert isinstance(page, int) and page_size > 0, "Cant be the 0!"
        try:
            start, end = index_range(page, page_size)
            return data[start:end]
        except IndexError:
            return []

    cond = Dict[str, Union[str, int, None, object]]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> cond:
        """
            We use that function for getting information which we could need
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        prev_page = page - 1 if page > 1 else None
        next_page = page + 1 if page < total_pages else None

        return {"page_size": page_size,
                "page": page, "data": data,
                "next_page": next_page,
                "prev_page": prev_page,
                "total_pages": total_pages}
