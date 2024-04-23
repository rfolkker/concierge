from shiny import App, ui, Inputs, Outputs, Session, reactive, render
from home import home_ui
from loader import loader_ui, loader_server
from prompter import prompter_ui, prompter_server
from collection_management import collection_management_ui, collection_management_server
from concierge_backend_lib.collections import get_collections
from shinyswatch._bsw5 import bsw5_themes
from shinyswatch import theme

UPLOADS_DIR = "uploads"

app_ui = ui.page_auto(
    ui.navset_pill_list(
        ui.nav_panel("Home", home_ui("home")),
        ui.nav_panel("Loader", loader_ui("loader")),
        ui.nav_panel("Prompter", prompter_ui("prompter")),
        ui.nav_panel("Collection Management", collection_management_ui("collection_management")),
        id="navbar"
    ), 
    ui.output_ui("theme_selector")  
)

def server(input: Inputs, output: Outputs, session: Session):

    selected_theme = reactive.value("cerulean")

    @render.ui
    def theme_selector():
        return ui.TagList(
            ui.input_select("selected_theme", "Theme", choices=bsw5_themes),
            theme.cerulean
        )

    selected_collection = reactive.value("")
    collections = reactive.value(get_collections())
    loader_server("loader", UPLOADS_DIR, selected_collection, collections)
    prompter_server("prompter", UPLOADS_DIR, selected_collection, collections)
    collection_management_server("collection_management", UPLOADS_DIR, selected_collection, collections)  


app = App(app_ui, server)

