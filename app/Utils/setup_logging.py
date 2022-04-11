import logging.config
import yaml
import os
import logging, logging.handlers

def setup_logging(
    default_path=r'Utils/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, mailhost, mailport, fromaddr, toaddrs, subject, capacity, pwd):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.mailhost = mailhost
        self.mailport = mailport
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.secure = None
        self.pwd = pwd

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                smtp.ehlo()
                smtp.starttls()
                smtp.login(self.fromaddr, self.pwd)
                msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (self.fromaddr, ",".join(self.toaddrs), self.subject)
                # msg = msg.encode("utf-8")
                for record in self.buffer:
                    s = self.format(record)
                    print(s)
                    msg = msg + s + "\r\n"
                smtp.sendmail(from_addr= self.fromaddr, to_addrs= self.toaddrs, msg=msg.encode("cp1252"))
                smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []
