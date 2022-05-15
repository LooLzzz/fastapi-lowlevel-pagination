# Fast Pagination

## Description

A lowlevel, fast and easy to use package for creating and managing your own pagination system while FastAPI.

Keeping the pagination system simple was the main goal of this package.  
You provide your own database querying logic and the pagination system will handle the rest.

## Example

### Imports

```py
import fast_pagination as pg
```

### Routes

```py
@router.get(..., response_model=pg.generate_response_schema(SomeModel))
async def some_route(
    pagination: pg.Pagination[SomeModel] = Depends(
        pg.get_pagination_dependency(offset_kwargs={...},
                                     limit_kwargs={...},
                                     filter_kwargs={...})
    ),
    ...  # additional route dependencies goes here
):
    return await pagination.paginate(
        func=db_query_func,
        ...  # func kwargs goes here
    )
```

### Services

```py
async def db_query_func(page_request: PageRequest, **extra_kwargs) -> dict:
    ...  # db query logic goes here

    return {
        'results': results,
        'total_items': total_items
    }
```
