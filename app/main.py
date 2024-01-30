# app/main.py
from flask import request
from flask_restful import Resource
from . import api, db
from .models import Alert
from .email import send_email,get_current_price

class MainResource(Resource):
    def get(self):
        return {'message': 'Welcome to Price Alert App!'}

class AlertResource(Resource):
    def get(self):
        # Fetch all alerts (you can implement pagination and filtering here)
        alerts = Alert.query.all()
        return {'alerts': [{'id': alert.id, 'cryptocurrency': alert.cryptocurrency,
                            'target_price': alert.target_price, 'status': alert.status} for alert in alerts]}

    def post(self):
        data = request.get_json()
        cryptocurrency = data.get('cryptocurrency')
        target_price = get_current_price(cryptocurrency)
        alert = Alert(cryptocurrency=cryptocurrency, target_price=target_price)
        if target_price>=33000:
            send_email(alert)

        
        try:
            alert = Alert(cryptocurrency=cryptocurrency, target_price=target_price)
            db.session.add(alert)
            db.session.commit()
            return {'message': 'Alert created successfully!'}
        except Exception:
            db.session.rollback()
            raise 'Alert already exists for the same cryptocurrency and target price.'
            
            
    def delete(self):
        data = request.get_json()
        alert_id = data.get('id')

        alert = Alert.query.get(alert_id)
        if alert:
            db.session.delete(alert)
            db.session.commit()
            return {'message': 'Alert deleted successfully!'}
        else:
            return {'message': 'Alert not found.'}, 404

api.add_resource(MainResource, '/')
api.add_resource(AlertResource, '/alerts')
