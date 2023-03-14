from fastapi import APIRouter, Depends, status

from .schemas import LamodaUrlSchema, SectionLimitGenderSchema
from .services import LamodaAPIDataService, LamodaParserService

router = APIRouter(prefix='/parse')


@router.post(
    '/api-scrapper',
    status_code=status.HTTP_200_OK
)
async def api_scrapper(
        schema: SectionLimitGenderSchema,
        service: LamodaAPIDataService = Depends()
):
    data = schema.dict()
    url = service.url.format(data.get('section'), data.get('limit'), data.get('gender'))
    new_data = service.get_all(url)
    service.create_lamoda_item(new_data.get('products'))
    return new_data


@router.post(
    '/scrapper',
    status_code=status.HTTP_200_OK
)
async def scrapper(
        schema: LamodaUrlSchema,
        service: LamodaParserService = Depends()
):
    url = schema.dict().get('url')
    response = service.get_response(url)
    goods = service.parser(response)
    service.insert_goods(goods)
    return goods
