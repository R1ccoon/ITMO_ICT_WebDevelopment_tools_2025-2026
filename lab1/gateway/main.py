import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from scalar_fastapi import Theme
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import text

from api import api_router
from config import app_settings, database_engine_async
from middlewares.permission import PermissionMiddleware
from schedulers.data_init import must_init

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("httpx").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if app_settings.FORCE_RESET_DATABASE:
            async with database_engine_async.begin() as conn:
                await conn.execute(text(f"DROP SCHEMA public CASCADE;"))
                await conn.execute(text(f"CREATE SCHEMA public;"))
            logging.info("Database has been reset to base state")

        proc = await asyncio.create_subprocess_exec(
            "alembic",
            "upgrade",
            "head",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            logging.error(f"Alembic migration failed. ({stderr.decode()})")
            raise RuntimeError(f"Migration error: ({stderr.decode()})")

        logging.info(f"Database migrations applied successfully. ({stdout.decode()})")
        await must_init()

        yield
    finally:
        pass


main_app = FastAPI(
    title="Template API",
    description="...",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)


@main_app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=main_app.openapi_url,
        title=main_app.title + " - API Reference",
        authentication={"preferredSecurityScheme": ["OAuth2PasswordBearer"]},
        theme=Theme.ALTERNATE,
        persist_auth=True,
    )


main_app.include_router(api_router)


main_app.add_middleware(
    PermissionMiddleware,
)
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
