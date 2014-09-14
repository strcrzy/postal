from postal.lib.router import Router
router = Router()
receipts = []
updates = []

@router.match(from_=".*connect@watsi.org.*",
              subject=r"^Update on your donation to (?P<receiver>.*)$")
def process_update(msg, receiver=None):
    print("process_updates")
    updates.append(msg)


@router.match(from_=".*connect@watsi.org.*",
              subject=r"^Receipt for your donation to (?P<receiver>.*)$")
def process_receipt(msg, receiver=None):
    print("process_receipt")
    receipts.append(msg)