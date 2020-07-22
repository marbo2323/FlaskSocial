# database session registry object, configured from
# create_app factory
DbSession = scoped_session(
    sessionmaker(),
    # __ident_func__ should be hashable, therefore used
    # for recognizing different incoming requests
    scopefunc=_app_ctx_stack.__ident_func__
)


def create_app(name_handler, config_object):


    """
        Application factory

        :param name_handler: name of the application.
        :param config_object: the configuration object.
        """
app = Flask(name_handler)
app.config.from_object(config_object)
app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

global DbSession
# BaseQuery class provides some additional methods like
# first_or_404() or get_or_404() -- borrowed from
# mitsuhiko's Flask-SQLAlchemy
DbSession.configure(bind=app.engine, query_cls=BaseQuery)


@app.teardown_appcontext
def teardown(exception=None):
    globalDbSession
    if DbSession:
        DbSession.remove()

    return app


And
test
configuration
from conftest.py:

from our_application.globalimportcreate_app, DbSession


@pytest.yield_fixture(scope="session")
def app():
    """
    Creates a new Flask application for a test duration.
    Uses application factory `create_app`.
    """
    _app = create_app("testingsession", config_object=TestConfig)

    # Base is declarative_base()
    Base.metadata.create_all(bind=_app.engine)
    _app.connection = _app.engine.connect()

    # No idea why, but between this app() fixture and session()
    # fixture there is being created a new session object
    # somewhere.  And in my tests I found out that in order to
    # have transactions working properly, I need to have all these
    # scoped sessions configured to use current connection.
    DbSession.configure(bind=_app.connection)

    yield_app

    # the code after yield statement works as a teardown
    _app.connection.close()
    Base.metadata.drop_all(bind=_app.engine)


@pytest.yield_fixture(scope="function")
def session(app):
    """
    Creates a new database session (with working transaction)
    for a test duration.
    """
    app.transaction = app.connection.begin()

    # pushing new Flask application context for multiple-thread
    # tests to work
    ctx = app.app_context()
    ctx.push()

    session = DbSession()

    yield session

    # the code after yield statement works as a teardown
    app.transaction.close()
    session.close()
    ctx.pop()
