from persistencia import store
from menu import menu

def main():
    store.carregar_dados()
    try:
        menu()
    finally:
        # garante persistência final caso alterações tenham sido feitas durante o uso
        store.salvar_dados()

if __name__ == "__main__":
    main()
