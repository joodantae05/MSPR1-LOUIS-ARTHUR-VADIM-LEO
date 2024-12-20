from base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, root, app):
        title = "Page du Dashboard"
        tabs = {
            "Home": self.app.show_home_page,
            "Stats": self.app.show_stats_page,
            "Dashboard": self.app.show_dashboard_page,
            "Ping": self.app.show_ping_page
        }
        super().__init__(root, app, title, tabs)

        # Ajouter ici les éléments spécifiques au tableau de bord
