import imaplib
from email import message_from_string as parse_email
from collections import namedtuple


class Mailbox():
    """
    Mailbox is our interface to the specified IMAP mailbox.
    it can fetch all the messages from the box, and optionally
    it can delete them as well.
    """
    def __init__(self, host, user, password, mailbox="Inbox"):
        self.host = host
        self.user = user
        self.password = password
        self.mailbox = mailbox

    def delete_mail(self, *uids):
        conn.uid('STORE', ','.join(uids), '+FLAGS', r'(\Deleted)')

    def get_mail(self, delete=True):
        """
        fetches emails from the mailbox. 
        keyword arguments:
        delete - when True, deletes the messages after fetching them.
                 defaults to False
        """
        conn = imaplib.IMAP4_SSL(self.host)
        conn.login(self.user, self.password)
        conn.select(self.mailbox)
        search_result, search_data = conn.uid("search", None, "ALL")
        uids = search_data[0].split()
        message_count = len(uids)
        fetch_email = lambda uid: conn.uid('fetch', uid, '(RFC822)')[1][0][1]
        emails = [parse_email(fetch_email(uid)) for uid in uids]
        if(message_count and delete):
            delete_mail(uids)
        conn.expunge()
        conn.close()
        conn.logout()
        return emails
