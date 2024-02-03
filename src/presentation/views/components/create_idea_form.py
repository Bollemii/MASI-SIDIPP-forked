from consolemenu.prompt_utils import UserQuit

from src.domain.entities.community import Community
from src.domain.entities.idea import Idea
from src.presentation.views.generics.form import Form
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.icreate_idea import ICreateIdea


class CreateIdeaForm(Form):
    """Form to create an idea into a community"""

    def __init__(
        self, parent_menu: Menu, community: Community, create_idea_usecase: ICreateIdea
    ):
        super().__init__(parent_menu)
        self.community = community
        self.create_idea_usecase = create_idea_usecase

    def execute(self):
        """Executes the interaction with the user"""
        try:
            is_valid = False
            while not is_valid:
                idea_content = self._prompt_user(
                    "Décrivez votre idée", enable_quit=True
                )

                is_valid = len(idea_content) >= Idea.CONTENT_MIN_LENGTH
                if not is_valid:
                    self._print_error("L'idée doit contenir au moins 4 caractères.")

            result = self.create_idea_usecase.execute(
                self.community.identifier, idea_content
            )

            self._print_result_message(result)
        except UserQuit:
            pass
        except:
            self._print_error("Une erreur inconnue est survenue.")
        finally:
            self._prompt_to_continue()

    def _print_result_message(self, result: str):
        """Returns the message to display to the user"""
        if result == "Success!":
            self._print_success("Votre idée a été déposée avec succès !")
        else:
            self._print_error(
                f"Une erreur est survenue lors du dépôt de votre idée :\n{result}"
            )
