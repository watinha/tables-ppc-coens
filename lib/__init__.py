def generate_table_per_area (df, ch_opt, ch_unit, ch_at, ch_intern, ch_total):
  areas = {
    'Básico': df.loc[df['Núcleo'] == 'Básico'],
    'Específico': df.loc[df['Núcleo'] == 'Específico'],
    'Profissional': df.loc[df['Núcleo'] == 'Profissionalizante']
  }

  tex = '''
\begin{quadro}[ht!]
\caption{Representação da distribuição das unidades curriculares do curso por núcleo de conteúdo}
\label{tab:discarea}
\centering
\scriptsize
\begin{tabular}{|l|l|c|p{3.2cm}|}
\hline
\rowcolor{blue1}
Núcleo  & Unidades curriculares & CH [h]  & \% da CH da área em relação à CH das unidades curriculares do curso\\\hline
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
        tex += '\multirow{4}{*}{Núcleo %s} & %s & %d & %d horas  \\\n' % (k, unit['Nome'], unit['TOTAL'], ch_area)
      elif i == 1:
        tex += '\cline{2-3} & %s & %d & %d\%% (un. curriculares)\\\n' % (unit['Nome'], unit['TOTAL'], round((ch_area*100)/ch_unit))
      elif i == 2:
        tex += '\cline{2-3} & %s & %d & %d\%% (CH total)\\\n' % (unit['Nome'], unit['TOTAL'], round((ch_area*100)/ch_total))
      else:
        tex += '\cline{2-3} & %s & %d & \\\n' % (unit['Nome'], unit['TOTAL'])

  tex += '\multicolumn{2}{|l|}{\textbf{Carga Horária Total das Unidades Curriculares}} & \textbf{%d} &  \\\hline\n' % (ch_unit)
  tex += '\multicolumn{2}{|l|}{\textbf{Carga Horária de Atividades Complementares}} & \textbf{%d} &  \\\hline\n' % (ch_at)
  tex += '\multicolumn{2}{|l|}{\textbf{Carga Horária de Estágio Curricular Obrigatório}} & \textbf{%d} &  \\\hline\n' % (ch_intern)
  tex += '\multicolumn{2}{|l|}{\textbf{Carga Horária Total do Curso, incluindo AT, Estágio e TCC1/TCC2}} & \textbf{%d} & \\\hline' % (ch_total)
  tex += '''
\end{tabular}
\end{quadro}
'''

  with open('./tex/units_per_area.tex', 'w') as f:
    f.write(tex)


def generate_ead_table (required_df, ch_opt, ch_total):
  tex = '''\begin{quadro}[ht!]
\caption{Cargas horárias presencial e EaD }
\label{quad:ead}
\centering
\begin{tabular}{|l|c|c|}
\hline
\rowcolor{blue1}
 Modalidade &    Carga Horária  & \%\\
\hline
'''

  ch_ead = required_df.loc[:, 'NP'].sum() + ch_opt
  ch_presential = ch_total - ch_ead
  tex += 'Presencial & %d & %.2f \\\n' % (ch_presential, ((ch_presential/ch_total) * 100))
  tex += 'EaD & %d & %.2f \\\n' % (ch_ead, ((ch_ead/ch_total) * 100))
  tex += '\hline\nTotal  & %d & 100,00\\' % (ch_total)

  tex += '''\hline
\end{tabular}
\end{quadro}'''

  with open('./tex/ch_ead.tex', 'w') as f:
    f.write(tex)


