import flet as ft
from pathlib import Path
import json
import os

def get_assets_dir() -> Path:
    default_assets_dir = Path(__file__).parent / "assets"
    return Path(os.environ.get("FLET_ASSETS_DIR", str(default_assets_dir))).resolve()

def get_locales() -> dict:
    locales_dir = get_assets_dir() / "locales"
    languages = {}
    for file in locales_dir.glob("*.json"):
        lang = file.stem
        with open(file, "r", encoding="utf-8") as f:
            languages[lang] = json.load(f)
    return languages

async def main(page: ft.Page):
    device_info = await page.get_device_info()
    if device_info is None or not device_info.locales:
        lang = "en"
    else:
        lang = device_info.locales[0].language_code

    page.adaptive = True
    page.appbar = ft.AppBar(
        title=ft.Text("Classroom Status"),
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
