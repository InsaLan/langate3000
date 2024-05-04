\set user_name `echo ${LANGATE_USERNAME}`
\set test_user `echo ${LANGATE_USERNAME}_test`
\set user_pass `echo ${LANGATE_PASSWORD}`
\set db_name `echo ${LANGATE_DATABASE}`

CREATE USER :test_user WITH PASSWORD :'user_pass';
ALTER USER :test_user CREATEDB;

CREATE USER :user_name WITH PASSWORD :'user_pass';
CREATE DATABASE :db_name;
GRANT ALL ON DATABASE :db_name TO :user_name;
\c :db_name
GRANT USAGE, CREATE ON SCHEMA public TO :user_name;

