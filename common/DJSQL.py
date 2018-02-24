# -*- coding: utf-8 -*-
from django.db.models.sql.query import RawQuery
from django.db import connections
from django.db.models import Func, F

class RawQuerySet(object):
    """
    Provides an iterator which converts the results of raw SQL queries into
    annotated model instances.
    """
    def __init__(self, raw_query, params=None, query=None,
            translations=None, using=None, hints=None):
        self.raw_query = raw_query
        self.model = model
        self._db = using
        self._hints = hints or {}
        self.query = query or sql.RawQuery(sql=raw_query, using=self.db, params=params)
        self.params = params or ()
        self.translations = translations or {}

    def __iter__(self):
        # Cache some things for performance reasons outside the loop.
        db = self.db
        compiler = connections[db].ops.compiler('SQLCompiler')(
            self.query, connections[db], db
        )

        query = iter(self.query)

        try:
            for values in query:
                if converters:
                    values = compiler.apply_converters(values, converters)
                # Associate fields to values
                model_init_values = [values[pos] for pos in model_init_pos]
                instance = model_cls.from_db(db, model_init_names, model_init_values)
                if annotation_fields:
                    for column, pos in annotation_fields:
                        setattr(instance, column, values[pos])
                yield instance
        finally:
            # Done iterating the Query. If it has its own cursor, close it.
            if hasattr(self.query, 'cursor') and self.query.cursor:
                self.query.cursor.close()

    def __repr__(self):
        return "<RawQuerySet: %s>" % self.query

    def __getitem__(self, k):
        return list(self)[k]

    @property
    def db(self):
        "Return the database that will be used if this query is executed now"
        return self._db

    def using(self, alias):
        """
        Selects which database this Raw QuerySet should execute its query against.
        """
        return RawQuerySet(self.raw_query, model=self.model,
                query=self.query.clone(using=alias),
                params=self.params, translations=self.translations,
                using=alias)

    @property
    def columns(self):
        """
        A list of model field names in the order they'll appear in the
        query results.
        """
        if not hasattr(self, '_columns'):
            self._columns = self.query.get_columns()

            # Adjust any column names which don't match field names
            for (query_name, model_name) in self.translations.items():
                try:
                    index = self._columns.index(query_name)
                    self._columns[index] = model_name
                except ValueError:
                    # Ignore translations for non-existent column names
                    pass

        return self._columns


class UNIX_TIMESTAMP(Func):
    """
    把日期转换成时间戳
    """
    function = "UNIX_TIMESTAMP"

    def __init__(self, *expressions, **extra):
        if len(expressions) != 1:
            raise ValueError('DateSubtract must take only one expressions')
        super(UNIX_TIMESTAMP, self).__init__(*expressions, **extra)



