from tahrir_api.dbapi import TahrirDatabase
from tahrir_api.model import DBSession, DeclarativeBase
from sqlalchemy import create_engine


try:
    from subprocess import check_output as _check_output
    def check_output(cmd):
        try:
            return _check_output(cmd)
        except:
            return None
except:
    import subprocess
    def check_output(cmd):
        try:
            return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        except:
            return None

class TestDBInit(object):

    def setUp(self):
        check_output(['touch', 'testdb.db'])
        sqlalchemy_uri = "sqlite:///testdb.db"
        engine = create_engine(sqlalchemy_uri)
        DBSession.configure(bind=engine)
        DeclarativeBase.metadata.create_all(engine)

        self.api = TahrirDatabase(sqlalchemy_uri)

    def test_AddBadges(self):
        self.api.add_badge(
                "TestBadge",
                "TestImage",
                "A test badge for doing unit tests",
                "TestCriteria",
                1337
        )

        assert self.api.badge_exists("testbadge") == True

    def test_AddPerson(self):
        self.api.add_person(7331, "test@tester.com")
        assert self.api.person_exists("test@tester.com") == True

    def test_AddIssuer(self):
        _id = self.api.add_issuer(
                "TestOrigin",
                "TestName",
                "TestOrg",
                "TestContact"
        )
        assert self.api.issuer_exists("TestOrigin", "TestName") == True

    def tearDown(self):
        check_output(['rm', 'testdb.db'])
