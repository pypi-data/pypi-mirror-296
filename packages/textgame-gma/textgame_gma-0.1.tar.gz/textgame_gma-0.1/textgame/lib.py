class Game:
    class Ind:
        def __init__(self):
            self.state = self.gi()
        
        def gi(self):
            # Estado inicial do jogo
            ff = {
                "adder": [],
                "seles": {
                    "o1": {
                        'no': None
                    }
                }
            }
            return ff
        
        def init(self):
            # Inicializa o jogo
            self.state = self.gi()
            print("Game Initialized with state:", self.state)

        class Adder:
            def __init__(self):
                self.widgets = {}

            def addwi(self, widget_name: str, action=None):
                # Adiciona o widget e armazena a ação associada
                self.widgets[widget_name] = action
                print(f"Added widget: {widget_name}")
                if action:
                    action()  # Executa a ação associada ao widget

        class Sele:
            def __init__(self, options: list):
                self.options = options

            def is_digit(self, input_str: str):
                # Verifica se a entrada corresponde a algum item na lista de opções
                return input_str in self.options

    class TextGame:
        def __init__(self):
            self.ind = Game.Ind()
            self.adder = self.ind.Adder()
            self.sele = self.ind.Sele(["Start", "Options", "Exit"])

        def init(self):
            # Configura tudo necessário para o jogo
            self.ind.init()
            # Adiciona widgets com ações definidas
            self.adder.addwi("Button", action=self.on_button_click)
            self.adder.addwi("Option", action=self.on_option_click)
            # Manipula escolhas
            user_input = input("Enter an option: ")  # Recebe entrada do usuário
            if self.sele.is_digit(user_input):
                print(f"'{user_input}' is a valid option.")
            else:
                print(f"'{user_input}' is not a valid option.")

        def on_button_click(self):
            # Função de exemplo para a ação de um botão
            print("Button clicked!")

        def on_option_click(self):
            # Função de exemplo para a ação de uma opção
            print("Option selected!")

# Exemplo de uso
if __name__ == "__main__":
    game = Game.TextGame()
    game.init()
