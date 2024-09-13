model_input_sql = """
select 1 as id
"""

ephemeral_model_input_sql = """
{{ config(materialized='ephemeral') }}
select 2 as id
"""

raw_source_csv = """id
3
"""


model_sql = """
select *
from {{ ref('model_input') }}
union all
select *
from {{ ref('ephemeral_model_input') }}
union all
select *
from {{ source('seed_sources', 'raw_source') }}
"""


model_inline_sql = """
select * from {{ source('seed_sources', 'raw_source') }} as raw_source
"""

schema_sources_yml = """
sources:
  - name: seed_sources
    schema: "{{ target.schema }}"
    tables:
      - name: raw_source
"""


SEED = """
my_id,my_value
1,a
2,b
3,c
""".strip()


SCHEMA = """
version: 2

seeds:
  - name: my_seed
    description: "This is my_seed"
    columns:
      - name: id
        description: "This is my_seed.my_id"
"""

CONTROL = """
select * from {{ ref("my_seed") }}
"""


GET_COLUMNS_IN_RELATION = """
{{ config(materialized="table") }}
{% set columns = adapter.get_columns_in_relation(ref("my_seed")) %}
select * from {{ ref("my_seed") }}
"""


ALTER_COLUMN_TYPE = """
{{ config(materialized="table") }}
{{ alter_column_type(ref("my_seed"), "MY_VALUE", "varchar") }}
select * from {{ ref("my_seed") }}
"""


ALTER_RELATION_COMMENT = """
{{ config(
    materialized="table",
    persist_docs={"relations": True},
) }}
select * from {{ ref("my_seed") }}
"""


ALTER_COLUMN_COMMENT = """
{{ config(
    materialized="table",
    persist_docs={"columns": True},
) }}
select * from {{ ref("my_seed") }}
"""


ALTER_RELATION_ADD_REMOVE_COLUMNS = """
{{ config(materialized="table") }}
{% set my_seed = adapter.Relation.create(this.database, this.schema, "my_seed", "table") %}
{% set my_column = api.Column("my_column", "varchar") %}
{% do alter_relation_add_remove_columns(my_seed, [my_column], none) %}
{% do alter_relation_add_remove_columns(my_seed, none, [my_column]) %}
select * from {{ ref("my_seed") }}
"""


TRUNCATE_RELATION = """
{{ config(materialized="table") }}
{% set my_seed = adapter.Relation.create(this.database, this.schema, "my_seed", "table") %}
{{ truncate_relation(my_seed) }}
select * from {{ ref("my_seed") }}
"""
