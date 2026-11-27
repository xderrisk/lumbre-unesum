import flet as ft
from pathlib import Path
from dotenv import load_dotenv
from functools import cache
import json
import os

def get_assets_dir() -> Path:
    default_assets_dir = Path(__file__).parent / "assets"
    return Path(os.environ.get("FLET_ASSETS_DIR", str(default_assets_dir))).resolve()

@cache
def load_locale(lang: str) -> dict[str, str]:
    path = get_assets_dir() / "locales" / f"{lang}.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

async def main(page: ft.Page):
    load_dotenv(dotenv_path=get_assets_dir() / ".env")
    device_info = await page.get_device_info()
    locales = device_info.locales if device_info else []
    lang = locales[0].language_code if locales else "en"

    default = load_locale("en")
    t = default if lang == "en" else {**default, **load_locale(lang)}

    page.adaptive = True
    page.appbar = ft.AppBar(
        title=ft.Text(t["classroomStatusTitle"]),
        actions=[
            ft.IconButton(ft.Icons.INFO)
        ],
    )

    n = 6
    def grid_extent(width: float | None) -> int:
        w = width or 0
        if w >= 1200:
            return 400
        if w >= 1000:
            return 240
        return 170

    classrooms_gridview = ft.GridView(
        max_extent=grid_extent(page.width),
        child_aspect_ratio=1.2,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                border_radius=8,
            )
            for i in range(n)
        ],
    )

    def on_resize(_):
        classrooms_gridview.max_extent = grid_extent(page.width)
        page.update()

    page.on_resize = on_resize

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(
                padding=10,
                content=classrooms_gridview,
                alignment=ft.Alignment.CENTER,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
