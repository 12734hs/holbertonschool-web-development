#!/usr/bin/env python3
"""
We created that file for create the function for pagination
"""

def index_range(page=1, page_size=10):
    """
    We use that function for creating pagination main variables
    start we use for found out when the data starts
    end for find out when we have to stop show our data
    """
    start = (page - 1) * page_size
    end = start + page_size
    return start, end
