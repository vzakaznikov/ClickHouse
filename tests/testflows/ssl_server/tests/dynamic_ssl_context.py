import time

from testflows.core import *
from testflows.asserts import error
from ssl_server.requirements import *
from ssl_server.tests.common import *

@TestScenario
def enable_ssl(self):
    """Check enabling basic SSL server configuration.
    """
    with Given("I generate my own CA certificate"):
        bash = self.context.cluster.bash(node=None)

        my_own_ca_key_passphrase = "privet"
        my_own_ca_key= "my_own_ca.key"
        my_own_ca_crt = "my_own_ca.crt"
        server_key = "server.key"
        server_key_passpharase = "privet"
        server_csr = "server.csr"
        server_crt = "server.crt"

        with By("create my own CA key"):
            create_rsa_private_key(bash=bash, outfile=my_own_ca_key, passphrase=my_own_ca_key_passphrase)

        with And("create my own CA certificate"):
            create_ca_certificate(bash=bash, outfile=my_own_ca_crt, key=my_own_ca_key,
                passphrase=my_own_ca_key_passphrase, common_name="root")

        with And("generate server key"):
            create_rsa_private_key(bash=bash, outfile=server_key, passphrase=server_key_passpharase)

        with And("generate certificate signing request"):
            create_certificate_signing_request(bash=bash, outfile=server_csr, common_name="clickhouse1",
                key=server_key, passphrase=server_key_passpharase)

        with And("sign server certificate"):
            sign_certificate(bash=bash, outfile=server_crt, csr=server_csr,
                ca_certificate=my_own_ca_crt, ca_key=my_own_ca_key,
                ca_passphrase=my_own_ca_key_passphrase)

    # with Given("I add SSL server configuration file"):
    #     entries = {
    #         "openSSL": {
    #             "server": {
    #                 "certificateFile": "/etc/clickhouse-server/server.crt",
    #                 "privateKeyFile": "/etc/clickhouse-server/server.key",
    #                 "dhParamsFile": "/etc/clickhouse-server/dhparam.pem",
    #                 "verificationMode": "none",
    #                 "loadDefaultCAFile": "true",
    #                 "cacheSessions": "true",
    #                 "disableProtocols": "sslv2,sslv3",
    #                 "preferServerCiphers": "true"
    #             }
    #         }
    #     }
    #     add_ssl_server_configuration_file(entries=entries)

@TestFeature
@Name("dynamic ssl context")
@Requirements(
)
def feature(self, node="clickhouse1"):
    self.context.node = self.context.cluster.node(node)

    for scenario in loads(current_module(), Scenario):
        scenario()
