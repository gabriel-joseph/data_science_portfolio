ssh -L 9870:localhost:9870 \
    -L 8088:localhost:8088 \
    -L 8080:localhost:8080 \
    -L 18080:localhost:18080 \
    -L 16010:localhost:16010 \
    -L 8983:localhost:8983 \
    -L 8443:localhost:8443 \
    gvance67@34.61.213.179


ssh gvance67@34.61.213.179

URLs

Hadoop
http://localhost:9870/dfshealth.html#tab-overview

Spark
http://localhost:8080/

Spark History Server
http://localhost:18080/

Solr
http://localhost:8983/solr/#/

HBase
http://localhost:16010/master-status

Nifi
https://localhost:8443/nifi/

2025-12-07 17:11:47,154 WARN [main] o.a.nifi.properties.NiFiPropertiesLoader Generating Random Sensitive Properties Key [nifi.sensitive.props.key]
	org.apache.nifi.processors.standard.GenerateTableFetch
	org.apache.nifi.processors.standard.GenerateFlowFile
	org.apache.nifi.processors.standard.GenerateRecord
Generated Username [99d31e7b-89c8-4bbf-8c3a-b89160e6af4c]
Generated Password [rcbpzw2kAB+u4xGdFwURmH+/QuvdARla]
2025-12-07 17:11:44,548 INFO [main] org.apache.nifi.bootstrap.Command Generating Self-Signed Certificate: Expires on 2026-02-05
2025-12-07 17:11:46,297 INFO [main] org.apache.nifi.bootstrap.Command Generated Self-Signed Certificate SHA-256: D7A1E6F78C24264C447E17294274533DD19D6A769C5E63101106DD8C3F42432E



cd to dir then

docker compose up -d

