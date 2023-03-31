import pandas as pd

from lib import generate_table_per_area, generate_ead_table, generate_ch_human_table, generate_units_table_per_period

CH_OPT = 180
CH_TCC1 = 30
CH_TCC2 = 90
CH_INTERN = 360
CH_AT = 180

df_required = pd.read_csv('./data/obrigatorias.csv')
df_opt = pd.read_csv('./data/optativas.csv')
CH_UNIT = df_required.loc[:, 'TOTAL'].sum() + CH_OPT
CH_TOTAL = CH_UNIT + CH_INTERN + CH_AT

generate_table_per_area(df_required, CH_OPT, CH_UNIT, CH_AT, CH_INTERN, CH_TOTAL)
generate_ead_table(df_required, CH_OPT, CH_TOTAL)
generate_ch_human_table(df_required, df_opt, CH_UNIT)
generate_units_table_per_period(df_required, df_opt, 8, CH_OPT)
