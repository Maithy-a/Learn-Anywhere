# clean_test.py
import flet as ft

print("🎯 Module location:", ft.__file__)
print("📦 Version:", ft.__version__)
print("🖼️  Icon:", ft.icons.ARROW_BACK)

def main(page):
    page.title = "Clean Flet Test"
    page.add(
        ft.Text("🎉 SUCCESS! Flet is WORKING!", size=24, color=ft.Colors.GREEN_700),
        ft.ElevatedButton("Click Me", on_click=lambda e: e.control.page.add(ft.Text("Button works!")))
    )

ft.app(target=main, port=8888, view=ft.WEB_BROWSER)