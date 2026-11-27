import flet as ft
from pathlib import Path
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

    classrooms = ft.Text(lang)

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(
                content=classrooms,
                alignment=ft.Alignment.CENTER,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
