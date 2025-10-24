import pytest
from playwright.sync_api import Page, expect

# ------------------------- FIXTURES ------------------------- #

# 1️⃣ Hooks Especiais do Pytest

# Executa uma vez para toda a sessão de testes

    # Hook chamado antes de qualquer teste ou fixture de sessão correr.
    # Usado para inicializações globais (ex.: configurar logging, limpar pastas, iniciar base de dados de teste).
def pytest_sessionstart(session):
    print("🌍 Sessão de testes iniciada")

    # Hook chamado depois de todos os testes e de todas as fixtures de sessão terem sido finalizados.
    # Ideal para relatórios finais, limpeza de recursos externos, envio de notificações, etc.
def pytest_sessionfinish(session, exitstatus):
    print("🌍 Sessão de testes finalizada")

# 2️⃣ Fixtures “Session” e “Module”

    # scope="session": executa 1x por sessão
    # scope="module":  executa 1x por ficheiro de teste.
    # autouse=True: aplicada automaticamente em cada teste, sem precisar passar como argumento
    # O código antes do yield é o setup, e o depois do yield é o teardown.

@pytest.fixture(scope="session", autouse=True)
def global_setup():
    print("✅ Setup global (session)")
    yield
    print("🧹 Teardown global (session)")

# Fixture por módulo (1x por ficheiro de teste)
@pytest.fixture(scope="module", autouse=True)
def module_setup():
    print("📦 Setup módulo")
    yield
    print("📦 Teardown módulo")


# 3️⃣ Fixture com “Function” (Padrão) e Autouse

    # scope="function" (padrão): executa antes e depois de cada função de teste.
    # page: Page: injeta a fixture do Playwright que abre uma nova aba/contexto.
    # Garante que cada teste começa na página-base https://playwright.dev/.

@pytest.fixture(scope="function", autouse=True)
def function_setup_teardown(page: Page):
    print("➡️ Setup de função")
    page.goto("https://playwright.dev/")
    yield
    print("⬅️ Teardown de função")


# 4️⃣ Fixture Personalizada
    
    # Fixture não-autouse, scope="function" (padrão)
    # Precisas de incluir custom_data como parâmetro no teste para a usar.s
    # Útil para fornecer dados mock ou configurações diversas

@pytest.fixture()
def custom_data():
    return {
        "name": "Gonçalo",
        "email": "goncalo@example.com"
    }


# ------------------------- TESTES ------------------------- #

# 5️⃣ Funções de Teste

    # Usa a fixture page (fornecida pelo plugin pytest-playwright).
    # Testa navegação principal e valida URLs.
    
def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")
    page.click("text=Docs")
    expect(page).to_have_url("https://playwright.dev/docs/intro")
    
    # Exemplo de como aceder à custom_data dentro do teste
    # Apenas corre se incluíres custom_data nos parâmetros

def test_custom_fixture(page: Page, custom_data):
    print(f"📬 Nome recebido da fixture: {custom_data['name']}")
    assert "Gonçalo" in custom_data['name']


# ------------------------- PARAMETRIZAÇÃO ------------------------- #

# 6️⃣ Parametrização de Testes

    # @pytest.mark.parametrize: cria várias instâncias do mesmo teste, com diferentes valores.
    # Cada par (path, expected_title) gera um sub-teste isolado.
    # Excelente para cobertura rápida de múltiplas rotas/páginas.

    # Primeiro teste: path="docs/intro" e expected_title="Installation".
    # Segundo teste: path="docs/test-runners" e expected_title="Test Runners". -> Nao existe
    # Terceiro teste: path="docs/api/class-page" e expected_title="Page"

@pytest.mark.parametrize("path, expected_title", [
    ("docs/intro", "Installation"),
    ("docs/test-runners", "Test Runners"),
    ("docs/api/class-page", "Page")
])
def test_pages_titles(page: Page, path, expected_title):
    url = f"https://playwright.dev/{path}"
    page.goto(url)
    expect(page.locator("h1")).to_have_text(expected_title)
