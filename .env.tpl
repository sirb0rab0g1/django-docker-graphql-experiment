# dockerfile configuration
API=graphql-best-api
NGINX=graphql-best-nginx
REDIS=graphql_best_redis
POSTGRESQL=graphql_best_postgresql
PGADMINCONTAINER=graphql_best_pgadmin

#settings.py configuration
FLEX_HOST=0.0.0.0
IP_HOST=192.168.0.147
LOCAL_HOST=localhost

#PORTS
PORT=8001
REDIS_PORT=6380
PG_PORT=5433

# HOSTS=192.168.0.147,localhost,192.168.1.4
# CORS=192.168.0.147:8000,localhost:8000,192.168.0.147:4200,localhost:4200,192.168.1.4:4200

# SECRET_KEY=i1(s6dud&*%mke$t=49m6o8itzv@mlo8=zx4hct-i&=$tv9704
ENV=local

# DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
# REDIS_URL=redis://192.168.0.147:6379