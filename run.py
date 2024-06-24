from app import create_app, db

app = create_app()

# Initialisation de la base de données
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
