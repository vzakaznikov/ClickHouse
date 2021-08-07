from testflows.core import *
from helpers.common import *


@TestStep(Given)
def add_ssl_server_configuration_file(self, entries,
        config=None, config_d_dir="/etc/clickhouse-server/config.d",
        config_file="ssl_server.xml", timeout=300, restart=False):
    """Add SSL server configuration to config.xml.
    """
    if config is None:
        config = create_xml_config_content(entries, config_file=config_file, config_d_dir=config_d_dir)

    return add_config(config, timeout=timeout, restart=restart)


@TestStep(Given)
def add_ssl_client_configuration_file(self, entries,
        config=None, config_d_dir="/etc/clickhouse-server/config.d",
        config_file="ssl_client.xml", timeout=300, restart=False):
    """Add SSL client configuration to config.xml.
    """
    if config is None:
        config = create_xml_config_content(entries, config_file=config_file, config_d_dir=config_d_dir)

    return add_config(config, timeout=timeout, restart=restart)


@TestStep(Given)
def create_rsa_private_key(self, bash, outfile, passphrase, algorithm="aes256", length=2048):
    """Generate RSA private key.
    """
    try:
        with bash(f"openssl genrsa -{algorithm} -out {outfile} {length}", name="openssl", asynchronous=True) as cmd:
            cmd.app.expect(f"Enter pass phrase for.*?:")
            cmd.app.send(passphrase)
            cmd.app.expect("Verifying - Enter pass phrase for .*?:")
            cmd.app.send(passphrase)

        yield outfile

    finally:
        with Finally("I remove private key file"):
            bash(f"rm -rf \"{outfile}\"")


@TestStep(Given)
def create_ca_certificate(self, bash, key, passphrase, common_name,
        outfile, type="x509", days="3650",
        hash="sha256", extensions="v3_ca",
        country_name="", state_or_province="", locality_name="",
        organization_name="", organization_unit_name="",
        email_address=""):
    """Generate CA certificate.
    """
    try:
        with bash(f"openssl req -new -{type} -days {days} -key {key} "
                f"-{hash} -extensions {extensions} -out {outfile}", name="openssl", asynchronous=True) as cmd:
            cmd.app.expect("Enter pass phrase for.*?:")
            cmd.app.send(passphrase)
            cmd.app.expect("Country Name.*?:")
            cmd.app.send(country_name)
            cmd.app.expect("State or Province Name.*?:")
            cmd.app.send(state_or_province)
            cmd.app.expect("Locality Name.*?:")
            cmd.app.send(locality_name)
            cmd.app.expect("Organization Name.*?:")
            cmd.app.send(organization_name)
            cmd.app.expect("Organizational Unit Name.*?:")
            cmd.app.send(organization_unit_name)
            cmd.app.expect("Common Name.*?:")
            cmd.app.send(common_name)
            cmd.app.expect("Email Address.*?:")
            cmd.app.send(email_address)

        yield outfile

    finally:
        with Finally("I remove CA certificate file"):
            bash(f"rm -rf \"{outfile}\"")


@TestStep(Given)
def create_certificate_signing_request(self, bash, outfile, key, passphrase, common_name, hash="sha256",
        country_name="", state_or_province="", locality_name="",
        organization_name="", organization_unit_name="",
        email_address="", challenge_password="", company_name=""):
    """Generate certificate signing request.
    """
    try:
        with bash(f"openssl req -{hash} -new -key {key} -out {outfile}", name="openssl",
                asynchronous=True) as cmd:
            cmd.app.expect("Enter pass phrase for.*?:")
            cmd.app.send(passphrase)
            cmd.app.expect("Country Name.*?:")
            cmd.app.send(country_name)
            cmd.app.expect("State or Province Name.*?:")
            cmd.app.send(state_or_province)
            cmd.app.expect("Locality Name.*?:")
            cmd.app.send(locality_name)
            cmd.app.expect("Organization Name.*?:")
            cmd.app.send(organization_name)
            cmd.app.expect("Organizational Unit Name.*?:")
            cmd.app.send(organization_unit_name)
            cmd.app.expect("Common Name.*?:")
            cmd.app.send(common_name)
            cmd.app.expect("Email Address.*?:")
            cmd.app.send(email_address)
            cmd.app.expect("A challenge password.*?:")
            cmd.app.send(challenge_password)
            cmd.app.expect("An optional company name.*?:")
            cmd.app.send(company_name)


        yield outfile

    finally:
        with Finally("I remove certificate signing request file"):
            bash(f"rm -rf \"{outfile}\"")

@TestStep(Given)
def sign_certificate(self, bash, outfile, csr, ca_certificate, ca_key, ca_passphrase,
        type="x509", hash="sha256", days="365"):
    """Sign certificate using CA certificate.
    """
    try:
        with bash(f"openssl {type} -{hash} -req -in {csr} -CA {ca_certificate} "
                f"-CAkey {ca_key} -CAcreateserial -out {outfile} -days {days}",
                name="openssl", asynchronous=True) as cmd:
            cmd.app.expect("Enter pass phrase for.*?:")
            cmd.app.send(ca_passphrase)

        yield outfile

    finally:
        with Finally("I remove certificate file"):
            bash(f"rm -rf \"{outfile}\"")
