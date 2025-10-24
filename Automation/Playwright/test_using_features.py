import pytest
from playwright.sync_api import Page, expect

"""
    Page: representa a aba do navegador (fornecida por playwright).
    expect: é a forma moderna e legível de fazer asserts 

    @pytest.fixture: declara uma fixture.

    scope="function": será executada antes e depois de CADA FUNÇÃO de teste.

    autouse=True: essa fixture será automaticamente usada em cada teste, sem precisar passar como argumento.

    page: Page: o Playwright fornece a página já aberta para esta fixture.

    yield: Pausa a fixture aqui e executa o teste. Quando o teste termina, volta à fixture e executa o bloco após o yield (teardown).

    🔁 before_each_after_each (abre site)
        🔽
    ✅ test_main_navigation (verifica URL)
        🔽
    🧹 after_each_after_each (teardown)

"""


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    
    print("before the test runs")

    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")
    yield
    
    # Teardown
    print("after the test runs")

def test_main_navigation(page: Page):
    # Assertions use the expect API.
    expect(page).to_have_url("https://playwright.dev/")