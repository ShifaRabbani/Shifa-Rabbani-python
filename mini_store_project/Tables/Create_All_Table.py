
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_engine
from Tables.Invoice_table import create_invoice_table
from Tables.product_table import create_product_table
from Tables.Stock_table import create_stock_table
from Tables.user_table import create_user_table

conn = get_engine()
create_product_table(conn)
create_stock_table(conn)
create_invoice_table(conn)
create_user_table(conn)

print("Tables created successfully!")