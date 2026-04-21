from flask import Flask, jsonify

from routes.product_route import product_bp
from routes.stock_route import stck_bp
from routes.invoice_route import invoice_bp

