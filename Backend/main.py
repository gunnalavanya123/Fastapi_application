from fastapi import FastAPI
# from app.controllers.organizations_controllers import router as organizations_router
# from app.controllers.payments_controllers import router as payments_router
from app.controllers.supplier_controllers import router as supplier_router
from app.controllers.product_controllers import router as product_router
from app.controllers.email_controllers import router as mail_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# app.include_router(organizations_router)
# app.include_router(payments_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(mail_router)

origins=[
      'http://localhost:3000',
      "http://127.0.0.1:3000",
]

app.add_middleware(
      CORSMiddleware,
      allow_origins=origins,
      allow_credentials=True,
      allow_methods=['*'],
      allow_headers=['*']
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get('/')
async def home():
	return "Application Running..."
	


