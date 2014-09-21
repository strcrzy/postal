from glob import glob
from email import message_from_string as parse_email
from postal.lib.router import Router


def test_router_single_route_simple_match():
    emails = []
    router = Router()
    matched = []
    for filename in glob('./tests/fixtures/emails/*'):
        with open(filename) as f:
            emails.append(parse_email(f.read()))

    @router.match(from_=".*connect@watsi.org.*")
    def process(msg, receiver=None):
        assert(msg)
        matched.append(msg)

    assert(router.routes)
    assert(len(router.routes) is 1)
    for email in emails:
        router.route(email)
    assert(len(matched) is 2)
    receipt = matched[0]
    assert(receipt['Subject'] == 'Receipt for your donation to Tu Tu')
    update = matched[1]
    assert(update['Subject'] == 'Update on your donation to Maung Win')


def test_router_single_route_two_predicates():
    emails = []
    router = Router()
    receipts = []
    updates = []
    for filename in glob('./tests/fixtures/emails/*'):
        with open(filename) as f:
            emails.append(parse_email(f.read()))

    @router.match(from_=".*connect@watsi.org.*",
                  subject=r"^Update on your donation to (?P<receiver>.*)$")
    def process_update(msg, receiver=None):
        assert(receiver == 'Maung Win')
        updates.append(msg)
    assert(router.routes)
    print router.routes
    assert(len(router.routes) is 1)
    for email in emails:
        router.route(email)
    print(receipts)
    assert(len(updates) is 1)
    update = updates[0]
    assert(update['Subject'] == 'Update on your donation to Maung Win')


def test_router_two_routes_two_predicates():
    emails = []
    router = Router()
    receipts = []
    updates = []
    for filename in glob('./tests/fixtures/emails/*'):
        with open(filename) as f:
            emails.append(parse_email(f.read()))

    @router.match(from_=".*connect@watsi.org.*",
                  subject=r"^Update on your donation to (?P<receiver>.*)$")
    def process_update(msg, receiver=None):
        assert(receiver == 'Maung Win')
        updates.append(msg)

    @router.match(from_=".*connect@watsi.org.*",
                  subject=r"^Receipt for your donation to (?P<receiver>.*)$")
    def process_receipt(msg, receiver=None):
        assert(receiver == 'Tu Tu')
        receipts.append(msg)
    assert(router.routes)
    print router.routes
    assert(len(router.routes) is 2)
    for email in emails:
        router.route(email)
    print(receipts)
    assert(len(receipts) is 1)
    receipt = receipts[0]
    assert(receipt['Subject'] == 'Receipt for your donation to Tu Tu')
    assert(len(updates) is 1)
    update = updates[0]
    assert(update['Subject'] == 'Update on your donation to Maung Win')
