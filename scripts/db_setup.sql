CREATE DATABASE knowledgellm;
CREATE ROLE knowledgellm;
ALTER ROLE knowledgellm PASSWORD 'knowledgellm';
ALTER ROLE knowledgellm WITH LOGIN;
GRANT CONNECT ON DATABASE knowledgellm TO knowledgellm;
GRANT USAGE ON SCHEMA public TO knowledgellm;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO knowledgellm;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO knowledgellm;
ALTER USER knowledgellm CREATEDB;