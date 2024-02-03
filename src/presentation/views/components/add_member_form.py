from consolemenu.prompt_utils import UserQuit

from src.domain.entities.community import Community
from src.presentation.views.generics.form import Form
from src.presentation.views.generics.menu import Menu
from src.application.interfaces.iadd_member import IAddMember
from src.application.interfaces.imachine_service import IMachineService


class AddMemberForm(Form):
    """Form to add a member to a community"""

    def __init__(
        self,
        parent_menu: Menu,
        community: Community,
        add_member_usecase: IAddMember,
        machine_service: IMachineService,
    ):
        super().__init__(parent_menu)
        self.community = community
        self.add_member_usecase = add_member_usecase
        self.machine_service = machine_service

    def execute(self):
        """Executes the interaction with the user"""
        try:
            is_valid = False
            while not is_valid:
                ip_address = self._prompt_user(
                    "Adresse IP du nouveau membre", enable_quit=True
                )

                values = ip_address.split(".")
                is_valid = len(values) == 4
                is_valid = is_valid and all(value.isdigit() for value in values)
                is_valid = is_valid and all(0 <= int(value) <= 255 for value in values)

                if not is_valid:
                    self._print_error(
                        "L'adresse IP est invalide (format : 255.255.255.255)."
                    )

            result = self.add_member_usecase.execute(
                self.community.identifier,
                ip_address,
                self.machine_service.get_port(),
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
            self._print_success("Le membre a été ajouté avec succès!")
        else:
            self._print_error(
                f"Une erreur est survenue lors de l'ajout du membre :\n {result}"
            )
