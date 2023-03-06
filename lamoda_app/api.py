from fastapi import APIRouter, Depends, status

from .schemas import SectionLimitGenderSchema
from .services import LamodaAPIDataService

router = APIRouter(prefix='/parse')


@router.post(
    '/scrapper',
    status_code=status.HTTP_200_OK
)
async def scrapper(
        schema: SectionLimitGenderSchema,
        service: LamodaAPIDataService = Depends()
):
    data = schema.dict()
    url = "https://www.lamoda.ru/api/v1/recommendations/section?section={0}&limit={1}&gender={2}"
    url = url.format(data.get('section'), data.get('limit'), data.get('gender'))
    res = service.get_all(url)
    return res
