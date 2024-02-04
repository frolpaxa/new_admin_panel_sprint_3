from time import sleep

import psycopg2
from psycopg2.extras import RealDictCursor

from backoff import backoff
from configuration import Config
from es_uploader import EsUploader
from pg_loader import PgLoader
from queries import GENRES, MOVIES, PERSONS
from state import JsonFileStorage, State

ENTITY = {
    "film_work": MOVIES,
    "person": PERSONS,
    "genre": GENRES,
}


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10)
def run(conf: Config):
    try:
        with psycopg2.connect(dsn=conf.pg_dsn) as conn, conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:
            loader = PgLoader(cur, conf.pack_size)
            uploader = EsUploader(conf.es_url, conf.es_index)
            state = State(JsonFileStorage(file_path=conf.file_storage))
            modified = state.get_state("modified") or conf.start_date

            for query in ENTITY.values():
                for data, last_updated in loader.read_data(query, modified):
                    uploader.upload(data)

        state.set_state("modified", str(last_updated))

    finally:
        sleep(conf.sleep_time)


if __name__ == "__main__":
    while True:
        run(Config())
