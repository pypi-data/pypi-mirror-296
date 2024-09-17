import polars as pl

from tesseract_olap.exceptions.query import InvalidQuery
from tesseract_olap.query import DataQuery


def growth_calculation(query: DataQuery, df: pl.DataFrame):
    # define parameters
    measure = query.growth.measure
    method = query.growth.method

    time_name = query.growth.time
    try:
        time = next(
            lvlfi
            for hiefi in query.fields_qualitative
            for lvlfi in hiefi.drilldown_levels
            if lvlfi.name == time_name
        )
    except StopIteration:
        msg = f"Time level '{time_name}' is required as a drilldown for its own growth calculation"
        raise InvalidQuery(msg) from None

    time_id = (
        time.name
        if time.level.get_name_column(query.locale) is None
        else f"{time.name} ID"
    )

    list_drilldowns = list(df.columns)
    list_drill_without_time_measure = [
        col for col in list_drilldowns if col not in {time_name, time_id, measure}
    ]

    if method[0] == "period":
        amount = method[1]

        # create column with 'previous measure'
        df_current = df.with_columns([(pl.col(time_id) - amount).alias("time_prev")])

        df = df_current.join(
            # filter the time_prev column string if it exists
            df.select(list_drill_without_time_measure + [time_id, measure]).rename(
                {time_id: "time_prev", measure: "previous_measure"}
            ),
            on=list_drill_without_time_measure + ["time_prev"],
            how="left",
        )

    else:
        type_caster = time.level.key_type.get_caster()
        member_key = type_caster(method[1])

        if len(list_drill_without_time_measure) == 0:
            # create a "dummy" column in case there are no columns for the join
            df = df.with_columns([pl.lit(1).alias("dummy")])

            list_drill_without_time_measure.append("dummy")

        # first, we get the values ​​at fixed time per group
        df_fixed = (
            df.filter(pl.col(time_id) == member_key)
            .select(list_drill_without_time_measure + [measure])
            .rename({measure: "previous_measure"})
        )

        # join the fixed values ​​to the original df
        df = df.join(df_fixed, on=list_drill_without_time_measure, how="left")

    df = df.with_columns(
        [
            # calculate the absolute change
            (pl.col(measure) - pl.col("previous_measure")).alias(
                f"{measure} Growth Value"
            ),
            # calculate the percentage change
            (
                (pl.col(measure) - pl.col("previous_measure"))
                / pl.col("previous_measure")
            ).alias(f"{measure} Growth"),
        ]
    )

    # remove temporary column 'previous measure' and 'dummy'
    columns_to_drop = ["previous_measure", "time_prev", "dummy"]
    existing_columns = [col for col in columns_to_drop if col in df.columns]
    df = df.drop(existing_columns)

    return df
