from app import create_app


# pylint: disable=C0103
# invalid-name
app = create_app()

if __name__ == '__main__':
    app.run()
# pylint: enable=C0103
