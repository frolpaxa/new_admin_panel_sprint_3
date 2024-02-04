from models import Person


def enc_s(value):
    """
    Какие-то приколы у ELK с кодировкой для экзотического текста (некогда уже разбираться...)
    """

    return value.encode("ascii", "ignore").decode("ascii") if value else value


def transform_data(data):
    """
    Собираем необходимую структуру данных
    """

    actors = [
        Person(person_id=x["person_id"], person_name=enc_s(x["person_name"]))
        for x in data.get("persons")
        if x.get("person_role") == "actor"
    ]
    writers = [
        Person(person_id=x["person_id"], person_name=enc_s(x["person_name"]))
        for x in data.get("persons")
        if x.get("person_role") == "writer"
    ]

    return data | dict(
        title=enc_s(data.get("title")),
        description=enc_s(data.get("description")),
        director=" ".join(
            [
                enc_s(x.get("person_name"))
                for x in data.get("persons")
                if x.get("person_role") == "director"
            ]
        ).strip(),
        actors_names=" ".join([person.name for person in actors]),
        writers_names=[person.name for person in writers],
        actors=actors,
        writers=writers,
    )
