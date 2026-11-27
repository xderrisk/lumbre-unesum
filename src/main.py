import flet as ft


def main(page: ft.Page):
    page.adaptive = True
    page.appbar = ft.AppBar(
        title=ft.Text("Classroom Status"),
        actions=[
            ft.IconButton(ft.Icons.INFO)
        ],
    )

    classrooms = ft.Text("0", size=50, data=0)

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
