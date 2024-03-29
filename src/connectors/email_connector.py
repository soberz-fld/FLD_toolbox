import smtplib
import email.message


class EmailConnector:
    _smtp_server, _smtp_port, _smtp_username, _smtp_password, _from_address, _from_name = None, None, None, None, None, None
    _smtp_handler = None

    def __init__(
            self,
            smtp_server: str,
            smtp_port: int,
            smtp_username: str,
            smtp_password: str,
            from_address: str,
            from_name: str = None
    ):
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._smtp_username = smtp_username
        self._smtp_password = smtp_password
        self._from_address = from_address
        self._from_name = from_name

        if smtp_server == '' or smtp_server is None or smtp_port == 0 or smtp_port is None or smtp_username == '' or smtp_username is None or from_address == '' or from_address is None:
            raise ValueError('Server, Port or Username incorrect or missing: Maybe it is None or an empty string?')

        # Initializing SMTP object
        self._smtp_handler = smtplib.SMTP_SSL(self._smtp_server, self._smtp_port)

    def send_email(self, subject: str, content: str, to: list[str] = None, cc: list[str] = None, bcc: list[str] = None, content_is_html: bool = False):  # TODO: Return something

        self._smtp_handler.ehlo()
        self._smtp_handler.login(self._smtp_username, self._smtp_password)

        # Creating msg object
        msg = email.message.EmailMessage()
        # Setting content
        if content_is_html:
            msg.set_content(content, subtype='html')
        else:
            msg.set_content(content)
        # Setting other meta data
        msg['Subject'] = subject
        if self._from_name != '' and self._from_name is not None and self._from_address != '' and self._from_address is not None:
            msg['From'] = str(self._from_name) + '<' + str(self._from_address) + '>'
        elif self._from_address != '' and self._from_address is not None:
            msg['From'] = str(self._from_address) + '<' + str(self._from_address) + '>'
        elif self._from_name != '' and self._from_name is not None:
            msg['From'] = str(self._from_name) + '<' + str(self._smtp_username) + '>'
        else:
            msg['From'] = str(self._smtp_username) + '<' + str(self._smtp_username) + '>'
        msg['To'] = self._create_string_of_recipients_of_list(to)
        msg['Cc'] = self._create_string_of_recipients_of_list(cc)
        msg['Bcc'] = self._create_string_of_recipients_of_list(bcc)

        if msg['To'] == '' and msg['Cc'] == '' and msg['Bcc'] == '':
            raise ValueError('No recipient')

        self._smtp_handler.send_message(msg)
        self._smtp_handler.close()

    def _create_string_of_recipients_of_list(self, list_of_recipients: list[str]) -> str:
        """
        Creates a string of recipient's email addresses with a comma as delimiter.
        :param list_of_recipients: List of strings with recipients
        :return: String of all recipient's email addresses in one string to use in object of email.message.EmailMessage()
        """
        if list_of_recipients:
            string_of_recipients = ''
            for recipient in list_of_recipients:
                if string_of_recipients != '':
                    string_of_recipients += ', '
                string_of_recipients += recipient
            return string_of_recipients
        else:
            return ''
