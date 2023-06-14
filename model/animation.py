class Animation:
    def __init__(self, title_kr, title_origin, genre, director, airing_period, production_company):
        self.title_kr = title_kr
        self.title_origin = title_origin
        self.genre = genre
        self.director = director
        self.airing_period = airing_period
        self.production_company = production_company
    def save_to_database(self):
        # TODO: Save the animation data to the database
        print("Saving animation data to the database...")

    def save_to_file(self):
        # TODO: Save the animation data to a file
        print("Saving animation data to a file...")