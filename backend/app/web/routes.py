from aiohttp.web_app import Application


def setup_routes(app: Application):
    from app.admin.routes import setup_routes as admin_setup_routes
    from app.users.routes import setup_routes as user_setup_routes
    from app.ranks.routes import setup_routes as rank_setup_routes
    from app.positions.routes import setup_routes as position_setup_routes
    from app.problems.routes import setup_routes as problem_setup_routes
    #from app.products.routes import setup_routes as product_setup_routes
    from app.partners.routes import setup_routes as partner_setup_routes
    from app.addresses.routes import setup_routes as addresse_setup_routes
    from app.jobs.routes import setup_routes as job_setup_routes
    from app.offices.routes import setup_routes as office_setup_routes
    from app.partner_params.routes import setup_routes as partner_param_setup_routes
    from app.todo.routes import setup_routes as todo_setup_routes

    admin_setup_routes(app)
    user_setup_routes(app)
    rank_setup_routes(app)
    position_setup_routes(app)
    problem_setup_routes(app)
    #product_setup_routes(app)
    partner_setup_routes(app)
    addresse_setup_routes(app)
    job_setup_routes(app)
    office_setup_routes(app)
    partner_param_setup_routes(app)
    todo_setup_routes(app)

