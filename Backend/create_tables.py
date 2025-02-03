from app.db.database import Base,engine
from app.model.organizations import Organizations
from app.model.roles import Roles
from app.model.miscellaneous import Miscellaneous
from app.model.user import User
from app.model.payments import Payments
from app.model.plans import Plan
from app.model.products import Product
from app.model.suppliers import Supplier

Base.metadata.create_all(engine)