"""
High-level interface for data access using Table Access Protocol (TAP)
"""


import os
import secrets
import shutil
import tempfile
import time
from io import BytesIO
from pathlib import Path
from typing import Callable, Dict, List, Literal, Sequence, Union
from urllib.parse import quote, urlencode

import numpy as np
import pandas as pd
import requests
from astropy import units as u
from astropy.table import Table
from astropy.units import Quantity
from bs4 import BeautifulSoup

from pylegs.config import configs
from pylegs.io import (PathOrFile, TableLike, _create_parents, _prepare_path,
                       concat_tables, download_file,
                       parallel_function_executor, read_table, write_table)
from pylegs.utils import guess_coords_columns, sanitize_quantity

__all__ = [
  'ls_crossmatch', 'sync_query', 'async_query', 'batch_sync_query', 
  'batch_async_query'
]

DEFAULT_CATALOG_COLUMNS = [
  'ra', 'dec', 'fracflux_r', 'fracin_r', 'fracmasked_r',
  'mag_g', 'mag_i', 'mag_r', 'mag_z',
  'nea_g', 'nea_i', 'nea_r', 'nea_z', 'nest4096', 'ngood_g', 'ngood_i', 
  'ngood_r', 'ngood_z', 'nobs_g', 'nobs_i', 'nobs_r', 'nobs_z', 'ring256', 
  'sersic', 'shape_e1', 'shape_e2', 'shape_r', 'snr_g', 'snr_i', 'snr_r', 
  'snr_z', 'type'
]

def ls_crossmatch(
  table: TableLike | PathOrFile, 
  columns: Sequence[str], 
  radius: float | u.Quantity,
  save_path: str | Path,
  ra_col: str = None,
  dec_col: str = None,
  overwrite: bool = False,
  cache_dir: str | Path = None,
  overwrite_cache: bool = False,
  workers: int = 3,
):
  if isinstance(save_path, (str, Path)) and Path(save_path).exists() and not overwrite:
    return
  
  query_template = """
  SELECT TOP 1 {columns}, 
    POWER((ra - ({ra})) * ({cos_dec}), 2) + POWER(dec - ({dec}), 2) AS ls_sep
  FROM ls_dr10.tractor
  WHERE 
    ls_sep < {radius}
  ORDER BY ls_separation ASC
  """.strip()
  df = read_table(table)
  ra_col, dec_col = guess_coords_columns(df, ra_col, dec_col)
  radius = sanitize_quantity(radius, u.arcsec, convert=True)
    
  queries = []
  for i, row in df.iterrows():
    ra = sanitize_quantity(row[ra_col], u.deg, convert=True)
    dec = sanitize_quantity(row[dec_col], u.deg, convert=True)
    query = query_template.format(
      columns=','.join([str(c) for c in columns]), 
      ra=ra.value,
      dec=dec.value,
      radius=radius.to(u.deg).value,
      cos_dec=np.cos(dec.to(u.rad).value),
    )
    queries.append(query)
  
  partial_paths = None
  if cache_dir is not None:
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    partial_paths = [cache_dir / f'{i}.csv' for i in range(len(queries))]
  
  batch_sync_query(
    queries=queries, 
    save_paths=save_path, 
    concat=True, 
    workers=workers,
    partial_paths=partial_paths,
    overwrite_partials=overwrite_cache,
  )


def sync_query(
  query: str, 
  save_path: PathOrFile = None,
  overwrite: bool = True,
  http_client: requests.Session = configs.HTTP_CLIENT,
  dtype: Literal['bytes', 'pandas', 'astropy'] = 'bytes'
) -> bytes | pd.DataFrame | Table:
  params = {
    'request': 'doQuery',
    'version': 1.0,
    'lang': 'ADQL',
    'phase': 'run',
    'format': 'csv',
    'query': query
  }
  save_path = _prepare_path(save_path)
  _create_parents(save_path)
  
  # req_url = configs.TAP_SYNC_BASE_URL + '?' + urlencode(params)
  table_bytes = None
  attempt = 0
  max_attempts = 5
  while table_bytes is None and attempt < max_attempts:
    table_bytes = download_file(
      url=configs.TAP_SYNC_BASE_URL,#req_url, 
      save_path=save_path, 
      overwrite=overwrite,
      query=params,
      http_client=http_client,
    )
    attempt += 1
  
  if dtype == 'bytes':
    return table_bytes
  if dtype in ('pandas', 'astropy'):
    return read_table(BytesIO(table_bytes), fmt='csv', dtype=dtype)


def async_query(
  query: str, 
  save_path: PathOrFile = None,
  overwrite: bool = True,
  http_client: requests.Session = configs.HTTP_CLIENT,
  delay: int = 5,
  dtype: Literal['bytes', 'pandas', 'astropy'] = 'bytes'
) -> bytes | pd.DataFrame | Table:
  params = {
    'request': 'doQuery',
    'version': 1.0,
    'lang': 'ADQL',
    'phase': 'run',
    'format': 'csv',
    'query': query
  }
  save_path = _prepare_path(save_path)
  _create_parents(save_path)
  
  table_bytes = None
  attempt = 0
  max_attempts = 5
  
  while table_bytes is None and attempt < max_attempts:
    resp = http_client.post(
      url=configs.TAP_ASYNC_BASE_URL,
      data=params,
    )
    soup = BeautifulSoup(resp.text, 'xml')
    
    job_id = soup.find('uws:jobId').text
    job_phase = soup.find('uws:phase').text
    table_bytes = None
    
    while job_phase == 'PENDING':
      time.sleep(delay)
      resp = http_client.get(configs.TAP_ASYNC_BASE_URL + f'/{job_id}')
      soup = BeautifulSoup(resp.text, 'xml')
      job_phase = soup.find('uws:phase').text
    
    if job_phase == 'COMPLETED':
      table_url = soup.find('#result').attrs['xlink:href']
      table_bytes = download_file(
        url=table_url, 
        save_path=save_path, 
        overwrite=overwrite, 
        http_client=http_client
      )
    attempt += 1
  
  if dtype == 'bytes':
    return table_bytes
  if dtype in ('pandas', 'astropy'):
    return read_table(BytesIO(table_bytes), fmt='csv', dtype=dtype)
  
  
def _batch_query(
  func: Callable,
  queries: Sequence[str],
  save_paths: Sequence[str | Path],
  func_args: Dict[str, None],
  workers: int = 3,
  concat: bool = False,
  partial_paths: Sequence[str | Path] | None = None,
):
  save_paths_aux = save_paths
  if concat:
    if partial_paths is None:
      tmp_folder = Path(tempfile.gettempdir()) / f'pylegs_tap_{secrets.token_hex(4)}'
      tmp_folder.mkdir(parents=True, exist_ok=True)
      save_paths_aux = [tmp_folder / f'{i}.csv' for i in range(len(queries))]
    else:
      save_paths_aux = [Path(i) for i in partial_paths]
      save_paths_aux[0].parent.mkdir(parents=True, exist_ok=True)
    
  params = [
    {
      'query': _query,
      'save_path': _save_path,
      **func_args,
    }
    for _query, _save_path in zip(queries, save_paths_aux)
  ]
  
  try:
    parallel_function_executor(
      func,
      params=params,
      workers=workers,
      unit='query',
      ignore_error=False,
    )

    if concat:
      combined_df = concat_tables([p for p in save_paths_aux if p.exists()])
      write_table(combined_df, save_paths)
      if partial_paths is None:
        shutil.rmtree(tmp_folder)
  except Exception as e:
    if concat and partial_paths is None:
      shutil.rmtree(tmp_folder)
    raise e


def batch_sync_query(
  queries: str, 
  save_paths: PathOrFile = None,
  overwrite: bool = True,
  concat: bool = False,
  workers: int = 3,
  http_client: requests.Session = configs.HTTP_CLIENT,
  partial_paths: Sequence[str | Path] | None = None,
  overwrite_partials: bool = False,
) -> bytes | pd.DataFrame | Table:
  args = {
    'overwrite': overwrite_partials if concat else overwrite,
    'http_client': http_client,
  }
  _batch_query(
    func=sync_query, 
    queries=queries, 
    save_paths=save_paths, 
    func_args=args, 
    workers=workers, 
    concat=concat,
    partial_paths=partial_paths,
  )
  
  
def batch_async_query(
  queries: str, 
  save_paths: PathOrFile = None,
  overwrite: bool = True,
  concat: bool = False,
  workers: int = 3,
  http_client: requests.Session = configs.HTTP_CLIENT,
  delay: int = 5,
  partial_paths: Sequence[str | Path] | None = None,
  overwrite_partials: bool = False,
) -> bytes | pd.DataFrame | Table:
  args = {
    'overwrite': overwrite,
    'http_client': http_client,
    'delay': delay,
  }
  _batch_query(
    func=async_query, 
    queries=queries, 
    save_paths=save_paths, 
    func_args=args, 
    workers=workers, 
    concat=concat,
    partial_paths=partial_paths,
  )



def download_catalog(
  save_path: PathOrFile,
  columns: Sequence[str] | None = None,
  ra_min: float | Quantity = 0,
  ra_max: float | Quantity = 360,
  delta_ra: float | Quantity = 10 * u.arcmin,
  table: str = 'ls_dr10.tractor',
  exclude_types: Sequence[str] | None = ['PSF'],
  magr_min: float = 10,
  magr_max: float = 21,
  dec_min: float | Quantity = -90,
  dec_max: float | Quantity = 90, 
  brick_primary: bool | None = True,
  overwrite: bool = False,
  workers: int = 6,
  tmp_folder: str | Path | None = None,
  overwrite_tmp: bool = False,
):
  """
  PSF, REX, DEV, EXP, SER  
  """
  if columns is None:
    columns = DEFAULT_CATALOG_COLUMNS
    
  filters = ''
  if brick_primary is not None:
    filters += f'AND brick_primary = {int(brick_primary)} '
  if exclude_types is not None:
    for t in exclude_types:
      filters += f"AND type != '{t.upper()}' "
  
  template = """
  SELECT {cols}
  FROM {table}
  WHERE ra BETWEEN {ra_min:.12f} AND {ra_max:.12f}
  AND dec BETWEEN {dec_min:.8f} AND {dec_max:.8f}
  AND mag_r BETWEEN {magr_min:.7f} AND {magr_max:.7f} 
  {filters}
  """.strip()
  
  print('Summary:')
  ra_min = sanitize_quantity(ra_min, u.deg, convert=True)
  ra_max = sanitize_quantity(ra_max, u.deg, convert=True)
  print(f'RA range: [{ra_min}, {ra_max}]')
  ra_min, ra_max = ra_min.value, ra_max.value
  
  dec_min = sanitize_quantity(dec_min, u.deg, convert=True)
  dec_max = sanitize_quantity(dec_max, u.deg, convert=True)
  print(f'DEC range: [{dec_min}, {dec_max}]')
  dec_min, dec_max = dec_min.value, dec_max.value

  delta_ra = sanitize_quantity(delta_ra, u.deg, convert=True)
  print(f'RA step: {delta_ra}')
  delta_ra = delta_ra.value
  
  queries = [
    template.format(
      cols=', '.join(columns), 
      table=table, 
      magr_min=magr_min, 
      magr_max=magr_max, 
      filters=filters,
      dec_min=dec_min,
      dec_max=dec_max,
      ra_min=_ra_min,
      ra_max=_ra_min + delta_ra,
    )
    for _ra_min in np.arange(ra_min, ra_max, delta_ra)
  ]
  
  tmp_paths = None
  if tmp_folder is not None:
    tmp_paths = [
      Path(tmp_folder) / f'query_{_ra:.6f}-{(_ra+delta_ra):.6f}.csv' 
      for _ra in np.arange(ra_min, ra_max, delta_ra)
    ]
  
  print('\nExample query:')
  print(queries[0])
  print(f'\nNumber of queries: {len(queries)}\n')
  
  return batch_sync_query(
    queries=queries, 
    save_paths=save_path, 
    overwrite=overwrite, 
    concat=True, 
    workers=workers,
    partial_paths=tmp_paths,
    overwrite_partials=overwrite_tmp,
  )




if __name__ == '__main__':
  # sync_query(
  #   'select top 10 psfdepth_g, psfdepth_r from ls_dr9.tractor where ra between 230.2939-0.0013 and 230.2939+0.0013 and dec between 29.7714-0.0013 and 29.7714+0.0013',
  #   url='https://datalab.noirlab.edu/tap/sync'
  # )
  # sync_query('select top 10 psfdepth_g, psfdepth_r from ls_dr9.tractor where ra between 230.2939-0.0013 and 230.2939+0.0013 and dec between 29.7714-0.0013 and 29.7714+0.0013')
  download_catalog(ra_min=120, ra_max=120*u.deg+2*u.arcmin, save_path='test.parquet', delta_ra=1*u.arcmin, magr_min=15, magr_max=16, overwrite=True)