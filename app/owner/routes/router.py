from fastapi import APIRouter
from app.owner.routes.team_api import router as team_router
from app.owner.routes.branch_api import router as branch_router
from app.owner.routes.medical_api import router as medical_reps_router
from app.owner.routes.supplier_api import router as supplier_router
from app.owner.routes.patient_api import router as patient_router, notes_router, reports_router
from app.owner.routes.appointment_api import router as appointment_router
from app.owner.routes.product_category_api import router as product_category_router
from app.owner.routes.laboratory_api import router as laboratory_router
from app.owner.routes.masteroption_api import router as masteroption_router
from app.owner.routes.product_api import router as product_router
from app.owner.routes.inventory_api import router as inventory_router
from app.owner.routes.prescription_api import router as prescription_router

router = APIRouter()

router.include_router(team_router)
router.include_router(branch_router)
router.include_router(medical_reps_router)
router.include_router(supplier_router)
router.include_router(patient_router)
router.include_router(notes_router)
router.include_router(reports_router)
router.include_router(appointment_router)
router.include_router(product_category_router)
router.include_router(laboratory_router)
router.include_router(masteroption_router)
router.include_router(product_router)
router.include_router(inventory_router)
router.include_router(prescription_router)

