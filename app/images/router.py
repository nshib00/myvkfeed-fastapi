import httpx
from fastapi import Query, APIRouter
from fastapi.responses import StreamingResponse, Response

router = APIRouter(prefix='/images', tags=['Изображения'])


@router.get("/proxy")
async def proxy_image(url: str = Query(...)):
    """
    Загружает картинку с внешнего URL и отдаёт её напрямую.
    Использование: <img src="images/proxy/?url=https://...">
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10.0)
            if resp.status_code != 200:
                return Response(content="Ошибка загрузки изображения", status_code=resp.status_code)
            
            content_type = resp.headers.get("content-type", "image/jpeg")
            return StreamingResponse(resp.aiter_bytes(), media_type=content_type)

    except httpx.ConnectTimeout:
        return Response(
            content="Ошибка: превышено время ожидания соединения",
            status_code=504
        )
    except httpx.ReadTimeout:
        return Response(
            content="Ошибка: превышено время ожидания ответа сервера",
            status_code=504
        )
    except Exception as e:
        return Response(content=f"Ошибка: {str(e)}", status_code=500)
