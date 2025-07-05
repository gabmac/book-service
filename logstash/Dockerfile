ARG ELASTIC_VERSION

# https://www.docker.elastic.co/
FROM opensearchproject/logstash-oss-with-opensearch-output-plugin:latest

RUN logstash-plugin install logstash-codec-json logstash-output-opensearch
# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
