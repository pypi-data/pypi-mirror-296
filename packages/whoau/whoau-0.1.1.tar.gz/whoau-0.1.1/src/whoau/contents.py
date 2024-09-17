# src/whoau/content.py

"""
Only the Content will be placed here
"""

from whoau.config import Parameters
from whoau.utils import custom_color
from whoau.localization import local_greeting

# config = Parameters()
color_main, color_sub, color_emp = custom_color()  # color


def introduce(local_greeting_message: str = "Welcome") -> str:
    return f"""{local_greeting_message}, Human and Non-Human Visitor!
This is Vision Engineer YeEun Hong, fascinated by how technology can breathe new life into normal days.

Boldly asking [{color_sub}]‘why’ and ‘why not’[/] has been my guiding principle up to this day.
Throughout my journey, I’ve gained diverse perspectives and insights from various fields.
Continuing it, I'm try to focus on the journey, not just the destination.

Thank you for visiting, Always welcome to new collaborations :)"""


def contact(config: dict) -> dict:
    contact = dict()
    contact["title"] = "Contact me 💻"
    contact["email"] = config.author.email
    contact["github"] = config.author.github
    contact["blog"] = config.author.blog
    return contact


def code() -> str:
    return """
    from four_years import Educator, Engineer, Researcher, Vision

    class Dotpie(nn.Module):
        def __init__(self):
            super(Dotpie, self).__init__()

            # Role
            self.educator   = Educator(driven = "sharing knowledge")
            self.engineer   = Engineer(driven = "contributing to open-source project")
            self.classifier = nn.Linear(365, 2)

        def forward(self, an):

            # Tech Stack
            educating   = self.educator(dotpie, volunteering = ["LLM as tool", "Web/Django"])
            engineering = self.engineer(dotpie, prefer = ["efficiency", "Document AI", "sLLM"])
            output = self.classifier((torch.cat(educating, engineering), 1))
            return output

    hello_world = Dotpie()
    """


def farewell(config: dict) -> str:
    return f"""
Thank you for having your time!
Feel free to contact me 👋

>  Github:  {config.author.github}
>  Email:   {config.author.email}
"""


def proceed() -> str:
    return f"""[{color_sub}]🔒 New Feature is Released! Why don't you try?[/]  (It won't install any other dependencies)"""


def contents(customize_location: bool) -> dict:
    config = Parameters()
    contents_dict = dict()
    greeting = local_greeting(customize_location)  # whoau/localization

    # combine
    contents_dict["introduce"] = introduce(greeting)
    contents_dict["contact"] = contact(config)  # title, email, github, blog
    contents_dict["code"] = code()
    contents_dict["farewell"] = farewell(config)
    contents_dict["proceed"] = proceed()
    return contents_dict


if __name__ == "__main__":
    print(contents())
