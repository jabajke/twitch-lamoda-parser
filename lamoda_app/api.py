from fastapi import APIRouter, Depends, HTTPException, status

from src.utils import send_to_kafka

from .schemas import LamodaUrlSchema, SectionLimitGenderSchema
from .services import (LamodaAPIDataService, LamodaOutputDataService,
                       LamodaParserService)

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
    if new_data.get('products') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lamoda is broke down, try again later"
        )
    else:
        send_to_kafka(
            goods=new_data.get('products'),
            partition=0
        )
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

    send_to_kafka(goods, partition=1)
    return goods


@router.get(
    '/lamoda-parser-data',
    status_code=status.HTTP_200_OK
)
async def lamoda_parser_data(
        service: LamodaOutputDataService = Depends(),
        limit: int = 10,
):
    return service.output_parser_data(limit)


@router.get(
    '/lamoda-api-data',
    status_code=status.HTTP_200_OK
)
async def lamoda_api_data(
        service: LamodaOutputDataService = Depends(),
        limit: int = 10,
):
    return service.output_api_data(limit)
