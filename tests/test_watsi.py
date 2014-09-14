from glob import glob
from email import message_from_string as parse_email

emails = []
for filename in glob('./tests/fixtures/emails/*'):
    with open(filename) as f:
        emails.append(parse_email(f.read()))
assert len(emails) is 3

def test():
    from .fixtures.watsi import *
    assert(router.routes)
    assert(len(router.routes) is 2)
    update_route, receipt_route = router.routes
    for email in emails:
        router.route(email)
    print(receipts)
    assert(len(receipts) is 1)
    assert(len(updates) is 1)
