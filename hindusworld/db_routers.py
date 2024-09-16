class RegisterRouter:
    """
    A router to control all database operations on models in the
    Login model.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read Login models go to gramadevata.
        """
        if model.__name__ == 'Register':
            return 'gramadevata'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write Login models go to gramadevata.
        """
        if model.__name__ == 'Register':
            return 'gramadevata'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the Login model is involved.
        """
        if obj1.__class__.__name__ == 'Register' or obj2.__class__.__name__ == 'Register':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the Login model only appears in the 'gramadevata' database.
        """
        if model_name == 'Register':
            return db == 'gramadevata'
        return db == 'default'