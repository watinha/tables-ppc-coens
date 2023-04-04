import re, chevron

def generate_table_per_area (df, ch_opt, ch_unit, ch_at, ch_intern, ch_total):
  areas = {
    'Básico': df.loc[df['Núcleo'] == 'Básico'],
    'Específico': df.loc[df['Núcleo'] == 'Específico'],
    'Profissional': df.loc[df['Núcleo'] == 'Profissionalizante']
  }

  tex = '''
\\begin{quadro}[ht!]
\caption{Representação da distribuição das unidades curriculares do curso por núcleo de conteúdo}
\label{tab:discarea}
\centering
\scriptsize
\\begin{tabular}{|l|l|c|p{3.2cm}|}
\hline
\\rowcolor{blue1}
Núcleo  & Unidades curriculares & CH [h]  & \% da CH da área em relação à CH das unidades curriculares do curso\\\\\hline
'''

  for k in areas:
    area = areas[k]
    ch_area = area['TOTAL'].sum()

    l = area.to_dict('records')
    if k == 'Profissional':
      ch_area += ch_opt
      l.append({ 'Nome': 'CH de unidades curriculares optativas da área a ser cursada', 'TOTAL': ch_opt })

    for i, unit in enumerate(l):
      if i == 0:
        tex += '\multirow{4}{*}{Núcleo %s} & %s & %d & %d horas  \\\\\n' % (k, unit['Nome'], unit['TOTAL'], ch_area)
      elif i == 1:
        tex += '\cline{2-3} & %s & %d & %d\%% (un. curriculares)\\\\\n' % (unit['Nome'], unit['TOTAL'], round((ch_area*100)/ch_unit))
      elif i == 2:
        tex += '\cline{2-3} & %s & %d & %d\%% (CH total)\\\\\n' % (unit['Nome'], unit['TOTAL'], round((ch_area*100)/ch_total))
      else:
        tex += '\cline{2-3} & %s & %d & \\\\\n' % (unit['Nome'], unit['TOTAL'])

    tex += '\hline\n'

  tex += '\multicolumn{2}{|l|}{\\textbf{Carga Horária Total das Unidades Curriculares}} & \\textbf{%d} &  \\\\\hline\n' % (ch_unit)
  tex += '\multicolumn{2}{|l|}{\\textbf{Carga Horária de Atividades Complementares}} & \\textbf{%d} &  \\\\\hline\n' % (ch_at)
  tex += '\multicolumn{2}{|l|}{\\textbf{Carga Horária de Estágio Curricular Obrigatório}} & \\textbf{%d} &  \\\\\hline\n' % (ch_intern)
  tex += '\multicolumn{2}{|l|}{\\textbf{Carga Horária Total do Curso, incluindo AT, Estágio e TCC1/TCC2}} & \\textbf{%d} & \\\\\hline' % (ch_total)
  tex += '''
\end{tabular}
\end{quadro}
'''

  with open('./tex/units_per_area.tex', 'w') as f:
    f.write(tex)


def generate_ead_table (required_df, ch_opt, ch_total):
  tex = '''\\begin{quadro}[ht!]
\caption{Cargas horárias presencial e EaD }
\label{quad:ead}
\centering
\\begin{tabular}{|l|c|c|}
\hline
\\rowcolor{blue1}
 Modalidade &    Carga Horária  & \%\\\\
\hline
'''

  ch_ead = required_df.loc[:, 'NP'].sum() + ch_opt
  ch_presential = ch_total - ch_ead
  tex += 'Presencial & %d & %.2f \\\\\n' % (ch_presential, ((ch_presential/ch_total) * 100))
  tex += 'EaD & %d & %.2f \\\\\n' % (ch_ead, ((ch_ead/ch_total) * 100))
  tex += '\hline\nTotal  & %d & 100,00\\\\' % (ch_total)

  tex += '''\hline
\end{tabular}
\end{quadro}'''

  with open('./tex/ch_ead.tex', 'w') as f:
    f.write(tex)


def generate_ch_human_table (df_required, df_opt, ch_unit):
  human_required = df_required.loc[df_required['Tipo'] == 'H'].to_dict('records')
  total_human = df_required.loc[df_required['Tipo'] == 'H'].loc[:, 'TOTAL'].sum()
  human_opt = df_opt.loc[df_opt['Tipo'] == 'H'].to_dict('records')

  tex = '''\\begin{quadro}[ht!]
\caption{Representação das unidades curriculares do ciclo de humanidades.}
\label{quad:humanities}
\centering
\\begin{tabular}{|l|c|c|}
\hline
\\rowcolor{blue1}
 Unidade Curricular &    Carga Horária  & \%\\\\
\hline
'''
  for unit in human_required:
    tex += '%s & %d & %.2f \\\\\n' % (unit['Nome'], unit['TOTAL'], (unit['TOTAL'] / ch_unit) * 100)

  tex += '\hline\n'

  for unit in human_opt:
    tex += '%s & %d & Optativa \\\\\n' % (unit['Nome'], unit['TOTAL'])

  tex += '\hline\n'

  tex += 'Total (Obrigatório) & %d & %.2f\\\\\n' % (total_human, (total_human / ch_unit) * 100)

  tex += '''\hline
\end{tabular}
\end{quadro}'''

  with open('./tex/ch_human.tex', 'w') as f:
    f.write(tex)


def generate_units_table_per_period(df_required, df_opt, periodo_opt, ch_opt):
  periodos = df_required['Período'].unique().tolist()

  for periodo in periodos:
    units = df_required.loc[df_required['Período'] == periodo].to_dict('records')

    if periodo == periodo_opt:
      opts = df_opt.to_dict('records')
      for opt in opts:
        opt['Nome'] = '%s (Optativa)' % (opt['Nome'])
        opt['opt'] = True

      units = units + opts

    tex = '''\\begin{quadro}[ht!]
\centering
'''
    tex += '\caption{Conteúdos Curriculares do %d$^o$ Período}' % (periodo)
    tex += '\label{qua:periodo%d}' % (periodo)
    tex += '''
\\begin{tabular}{|p{8.0cm}|c|c|c|c|c|}
\hline
'''
    tex += '\\rowcolor{blue1} %d$^o$ Período & \multicolumn{5}{|c|}{\centering Carga-horária (horas)} \\\\ \hline\n' % (periodo)
    tex += '\\rowcolor{blue1} Unidade Curricular & Prática & Teórica & Total & EaD & AAE \\\\ \hline\n'
    extensao = 0
    total = 0
    total_remoto = 0

    for unit in units:
      if ('opt' not in unit):
        total += unit['TOTAL']
        total_remoto += unit['NP']

      if unit['Tipo'] != 'E' and unit['Tipo'] != 'T':
        tex += '%s & %d & %d & %d & %d	&	0 \\\\	\hline\n' % (unit['Nome'], unit['TOTAL']/2, unit['TOTAL']/2, unit['TOTAL'], unit['NP'])
      elif unit['Tipo'] == 'E':
        tex += '%s & %d & 0 & %d & %d	&	%d \\\\	\hline\n' % (unit['Nome'], unit['TOTAL'], unit['TOTAL'], unit['NP'], unit['TOTAL'])
        extensao = unit['TOTAL']
      else:
        tex += '%s & %d & 0 & %d & %d	&	0 \\\\	\hline\n' % (unit['Nome'], unit['TOTAL'], unit['TOTAL'], unit['NP'])

    if periodo == periodo_opt:
      total += ch_opt
      total_remoto += ch_opt

    tex += 'CH total do período & \multicolumn{2}{p{3.3cm}|}{\cellcolor{blue1}} & %d & %d	&	%d \\\\ \hline\n\end{tabular} \end{quadro}' % (total, total_remoto, extensao)

    with open('./tex/periodo-%d.tex' % (periodo), 'w') as f:
      f.write(tex)


def generate_curricular_units (df_required, df_opt):
  opts = df_opt.to_dict('records')
  units = df_required.to_dict('records') + opts
  all_units = ''

  for i, unit in enumerate(units):

    periodo = str(unit['Período']) if str(unit['Período']) != '-' else 'Optativa'

    if periodo != 'Optativa':
      periodo = '%s$^o$' % (periodo)

    if unit['Tipo'] == 'E' or unit['Tipo'] == 'T':
      pratica_presencial = unit['P']
      teorica_presencial = 0
      total_presencial = pratica_presencial
      pratica_ead = unit['NP']
    else:
      pratica_presencial = round(unit['P'] / 2)
      teorica_presencial = round(unit['P'] / 2)
      total_presencial = pratica_presencial + teorica_presencial
      pratica_ead = unit['NP']

    tes = unit['Temas de estudo'].split('\n')
    tes = [ re.sub(' \(\d+h\)', '', te)[5:] for te in tes ]
    ementa = ' '.join(tes)

    params = {
      'nome': unit['Nome'],
      'id': 'unit_%d' % (i),
      'nucleo': unit['Núcleo'],
      'periodo': periodo,
      'presencial': '\XBox' if unit['P'] > 0 else '\Square',
      'ead': '\XBox' if unit['P'] == 0 else '\Square',
      'extensionista': '\XBox' if unit['Tipo'] == 'E' else '\Square',
      'nao_extensionista': '\XBox' if unit['Tipo'] != 'E' else '\Square',
      'requisitos': '', # unit['Pré-requisitos'],
      'pratica_presencial': pratica_presencial,
      'teorica_presencial': teorica_presencial,
      'total_presencial': total_presencial,
      'pratica_ead': pratica_ead,
      'total': unit['TOTAL'],
      'ementa': ementa
    }

    with open('templates/curricular_unit.tex') as f:
      all_units += chevron.render(f, params)



  with open('./tex/unidades_curriculares.tex', 'w') as f:
    f.write(all_units)


def generate_themes_and_results (df_required):
  units = df_required.to_dict('records')
  all_tex = ''

  for i, unit in enumerate(units):
    if unit['Nome'].startswith('Trabalho de Conclusão de Curso'): continue

    tex = '''
\\begin{quadro}[ht!]
  \centering
'''
    temas = [ '\\xitem %s' % (theme) for theme in unit['Temas de estudo'].split('\n') ]
    ras = [ '\\xitem %s' % (ra) for ra in unit['Resultados de aprendizagem'].split('\n') ]

    tex += '\caption{Unidade Curricular %s}\n' % (unit['Nome'])
    tex += '\label{unit_themes_ras_%d}\n' % (i)
    tex += '\\begin{tabular}{|p{5cm}|p{8cm}|}\hline\n'
    tex += '{\cellcolor{blue1} Unidade curricular} & %s\\\\\hline\n' % (unit['Nome'])
    tex += '{\cellcolor{blue1} Núcleo} & %s\\\\\hline\n' % (unit['Núcleo'])
    tex += '{\cellcolor{blue1} Carga-horária (Horas)} & %d\\\\\hline\n' % (unit['TOTAL'])
    tex += '\multicolumn{2}{|p{13cm}|}{{\cellcolor{blue1} Temas de Estudo}}\\\\\hline\n'

    for tema in temas:
      tex += '\multicolumn{2}{|p{13cm}|}{%s} \\\\\n' % (tema)

    tex += '\multicolumn{2}{|p{13cm}|}{{\cellcolor{blue1} Resultados de Aprendizagem}} \\\\\hline\n'

    for ra in ras:
      tex += '\multicolumn{2}{|p{13cm}|}{%s} \\\\\n' % (ra)

    tex += '''
	\end{tabular}
\end{quadro}'''

    all_tex += tex

  with open('./tex/themes_and_results.tex', 'w') as f:
    f.write(all_tex)


def generate_summary_table(df_required, df_opts, ch_opts, ch_at, ch_intern, ch_total):
  ch_required = df_required['TOTAL'].sum()
  ch_required_percent = round((ch_required / ch_total) * 100)
  ch_opt = ch_opts
  ch_ext = df_required.loc[df_required['Tipo'] == 'E']['TOTAL'].sum()
  ch_ext_percent = round((ch_ext / ch_total) * 100)
  ch_ead = df_required['NP'].sum() + ch_opts
  ch_ead_percent = round((ch_ead / ch_total) * 100)
  ch_unit = ch_required + ch_opts
  ch_min_humanities = round(ch_unit / 10)
  ch_humanities = df_required.loc[df_required['Tipo'] == 'H']['TOTAL'].sum()
  ch_humanities_opt = df_opts.loc[df_opts['Tipo'] == 'H']['TOTAL'].sum()
  ch_total_humanities = ch_humanities + ch_humanities_opt
  ch_min_ext = round(ch_total / 10)
  ch_max_ead = round(ch_total * 0.4)
  ch_ead_required = df_required['NP'].sum()
  ch_ead_opt = ch_opts
  ch_ead_present = df_required.loc[df_required['P'] > 0]['NP'].sum()

  params = {
    'ch_required': ch_required,
    'ch_opt': ch_opt,
    'ch_ext': ch_ext,
    'ch_ext_percent': ch_ext_percent,
    'ch_intern': ch_intern,
    'ch_ead': ch_ead,
    'ch_ead_percent': ch_ead_percent,
    'ch_total': ch_total,
    'ch_unit': ch_unit,
    'ch_min_humanities': ch_min_humanities,
    'ch_humanities': ch_humanities,
    'ch_humanities_opt': ch_humanities_opt,
    'ch_total_humanities': ch_total_humanities,
    'ch_min_ext': ch_min_ext,
    'ch_ext': ch_ext,
    'ch_max_ead': ch_max_ead,
    'ch_ead_required': ch_ead_required,
    'ch_ead_opt': ch_ead_opt,
    'ch_ead_present': ch_ead_present
  }

  with open('templates/summary_table.tex') as f:
    tex = chevron.render(f, params)

  with open('./tex/summary_table.tex', 'w') as f:
    f.write(tex)
