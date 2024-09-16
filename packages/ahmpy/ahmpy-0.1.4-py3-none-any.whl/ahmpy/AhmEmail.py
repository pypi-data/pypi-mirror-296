import smtplib
from email import utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


class AhmEmail():
    '''
    通过AhmEmail类发送email
    '''

    def __init__(self, username: str = '2569674866@qq.com', login_token: str = "zqoppgniszwqeaej", smtp_host: str = 'smtp.qq.com') -> None:
        '''
        初始化AhmEmail类
        username: 用户名
        login_token: 登录token
        smtp_host: smtp服务器地址
        '''
        self.username = username
        self.login_token = login_token
        self.smtp_host = smtp_host
        self.server = None

    def __enter__(self):
        '''用于with语句的上下文管理器'''
        self.server = smtplib.SMTP_SSL(self.smtp_host, 465)
        try:
            self.server.login(self.username, self.login_token)
        except smtplib.SMTPAuthenticationError:
            print("认证失败，请检查用户名和密码")
            raise
        except smtplib.SMTPException as e:
            print(f"无法连接到SMTP服务器: {e}")
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''确保在退出时关闭服务器连接'''
        if self.server:
            self.server.quit()

    def send_email(self, recipient: str, subject: str, body: str, attachment_files: list = None) -> None:
        '''
        发送邮件，选择性添加表格附件,表格数据必须为扁平结构\n
        recipient: 收件人邮箱地址\n
        subject: 邮件主题\n
        body: 邮件内容\n
        attachment_files: 附件文件列表
        '''
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 添加附件
            if attachment_files:
                for filename in attachment_files:
                    if os.path.exists(filename):
                        self._add_attachment(msg, filename)
                    else:
                        print(f"文件{filename}不存在，跳过")

            # 发送邮件
            self.server.sendmail(self.username, recipient, msg.as_string())
            print(f"邮件已发送至 {recipient}")
        except Exception as e:
            print(f"发送邮件失败: {e}")

    def _add_attachment(self, msg, filename):
        '''
        添加附件到邮件
        '''
        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)

            basename = os.path.basename(filename)
            encoded_filename = utils.encode_rfc2231(basename, charset='utf-8')

            part.add_header(
                'Content-Disposition',
                f"attachment; filename*={encoded_filename}"
            )
            msg.attach(part)


if __name__ == '__main__':
    with AhmEmail() as email:
        email.send_email('2569674866@qq.com', '测试邮件',
                         '这是一封测试邮件', ['b.txt', '你好.txt'])
