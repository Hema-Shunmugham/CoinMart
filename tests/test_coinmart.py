# coding=utf-8
import os
import pytest
from coinmart import coinmart
import tempfile


@pytest.fixture
def client(request):
    db_fd, coinmart.app.config['DATABASE'] = tempfile.mkstemp()
    coinmart.app.config['TESTING'] = True
    client = coinmart.app.test_client()
    with coinmart.app.app_context():
        coinmart.init_db()
    def teardown():
        os.close(db_fd)
        os.unlink(coinmart.app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_empty_db(client):
    rv = client.get('/')
    if __name__ == '__main__':
        assert b'Unbelievable. No watchlist created so far' in rv.data


def test_login_logout(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data

def test_login_logout1(client):
    rv = login(client, 'admin@uni.sydney.edu.au', 'default')
    assert b'Login Success!' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data

def test_login_incorrect_credentials(client):
    with client as c:
        rv = c.post('/login', data=dict(
            username='admin',
            password='test'
        ), follow_redirects=False)
    if __name__ == '__main__':
        assert b'Incorrect username or password' in rv.data


def test_register_login(client):
    with client as c:
        rv = login(client, 'admin', 'default')
        assert b'Login Success!' in rv.data
        rv = client.post('/register', data=dict(
            username='Test',
            password='Hema7067',
            email='Test@yahoo.com',
            cfm_password='Hema7067'
        ), follow_redirects=True)
        if __name__ == '__main__':
            assert b'You were successfully registered and have been logged in' in rv.data


def test_register_invalid_password(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/register', data=dict(
        username='test',
        password='test',
        email='test@yahoo.com',
        cfm_password='test'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number' in rv.data


def test_register_password_match(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/register', data=dict(
        username='Test',
        password='Svalli30',
        email='test@yahoo.com',
        cfm_password='Svalli301'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Passwords do not match' in rv.data


def test_registered_users(client):
    rv = login(client, coinmart.app.config['USERNAME'],
               coinmart.app.config['PASSWORD'])
    assert b'Login Success!' in rv.data
    rv = client.post('/register', data=dict(
        username='Test1',
        password='Hema7067',
        email='test@yahoo.com',
        cfm_password='Hema7067'
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'User already registered' in rv.data


def test_getExchangeRateIsFloat():
    with coinmart.app.app_context():
      assert isinstance(coinmart.exchange_rate('bitcoin', 'EUR'), object)


def test_getExchangeRateComparison():
    with coinmart.app.app_context():
      assert coinmart.exchange_rate('bitcoin', 'EUR') != coinmart.exchange_rate('bitcoin', 'AUD')


def test_getExchangeRateComparison2():
    with coinmart.app.app_context():
      assert coinmart.exchange_rate('ethereum', 'GBP') != coinmart.exchange_rate('bitcoin', 'GBP')

def test_add_watchlist_pair():
    with coinmart.app.app_context():
        coinmart.init_db()
        coinmart.get_db()
        coinmart.exchange_rate('bitcoin', 'EUR')
        with coinmart.app.test_client() as client:
          rv = client.post('/addpair?name=bitcoin&id=1')
          assert isinstance(coinmart.add_watchlist_pair_method('1', 'bitcoin', 'EUR'), object)
          if __name__ == '__main__':
            assert b'New pair added' in rv.data

def test_add_watchlist():
    with coinmart.app.app_context():
        coinmart.redirect('/addwatchlist')
        assert coinmart.redirect('/dashboard')


def test_create_watchlist(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/addwatchlist', data=dict(
        watchlistname="admin",
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'add watch list Success!' in rv.data

def test_delete_watchlist(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/addwatchlist', data=dict(
        watchlistname="admin",
    ), follow_redirects=True)
    assert b'add watch list Success!' in rv.data
    rv = client.get('/deletewatchlist?name=delete_admin')
    if __name__ == '__main__':
        assert b'delete watch list Success!' in rv.data

def test_user_watchlist(client):
    with client as c:
        rv = c.post('/login', data=dict(
            username='Test',
            password='Test_123'
        ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'Login Success!' in rv.data
        assert client.get('/')
        assert client.show_watchlists()

def test_addapair_in_a_watchlist(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.post('/addpair', data=dict(
        msg="admin bitcoin",
        currency="EUR"
    ), follow_redirects=True)
    if __name__ == '__main__':
        assert b'New pair added' in rv.data


def test_deleteapair_in_a_watchlist(client):
    rv = login(client, 'admin', 'default')
    assert b'Login Success!' in rv.data
    rv = client.get('/deletepair?name=admin_bitcoin_EUR')
    if __name__ == '__main__':
        assert b'delete Success!' in rv.data