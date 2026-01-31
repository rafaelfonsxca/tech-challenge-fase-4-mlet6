import math
from typing import TypeVar
from src.schemas import Page
from sqlalchemy.orm import Query

T = TypeVar('T')

def paginate(query: Query, page: int, page_size: int) -> Page[T]:
    """
    Paginate a list of items.

    Args:
        items (List[T]): The list of items to paginate.
        page (int): The current page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Page[T]: A Page object containing paginated results.
    """
    if page < 1:
        raise ValueError("Page number must be greater than 0")
    if page_size < 1:
        raise ValueError("Page size must be greater than 0")
    if page > 1000:
        page = 1000  # Limit to a maximum of 1000 pages
   
    total_items = query.count()
    if total_items == 0:
        return Page(
            total_items=0,
            total_pages=0,
            current_page=page,
            page_size=page_size,
            results=[]
        )
    
    total_pages = math.ceil(total_items / page_size)
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    return Page(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        page_size=page_size,
        results=items
    )