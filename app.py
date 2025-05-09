from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

# Настройка подключения к базе данных SQLite и Инициализация SQLAlchemy и миграций
app = Flask('Hardware Tracker')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hardware.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель данных для оборудования
class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hardware_part =db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'{self.hardware_part} - {self.price} Rubles'

# Главная страница — отображает всё оборудование и общую сумму    
@app.route('/')
def index():
    hardware_items = Hardware.query.all()
    total_price = sum(item.price for item in hardware_items)

    return render_template('index.html', hardware=hardware_items, total=total_price)

# Обработка POST-запроса для добавления нового оборудования
@app.route('/add', methods=['POST'])
def add_hardware():
    data = request.json
    new_item = Hardware(**data)
    db.session.add(new_item)
    db.session.commit()

    return 'DONE'

# Обработка POST-запроса для удаления всех записей из таблицы
@app.route('/clear', methods=['POST'])
def clear_all():
    db.session.query(Hardware).delete()
    db.session.commit()

    return 'Cleared'

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)





