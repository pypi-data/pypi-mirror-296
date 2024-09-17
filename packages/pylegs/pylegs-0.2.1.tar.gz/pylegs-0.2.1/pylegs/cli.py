from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Sequence

from astropy import units as u

from pylegs.cutout import batch_cutout
from pylegs.io import read_table
from pylegs.tap import DEFAULT_CATALOG_COLUMNS, download_catalog
from pylegs.utils import guess_coords_columns


def _is_numeric(value: str):
  try:
    float(value)
    return True
  except ValueError:
    return False


def handle_dlcat(args: Namespace):
  exclude = {'PSF', 'REX', 'DEV', 'EXP', 'SER'} - set([s.upper() for s in args.types])
  download_catalog(
    save_path=args.output,
    columns=args.cols,
    ra_min=args.ra[0],
    ra_max=args.ra[1],
    delta_ra=args.delta,
    table=args.table,
    exclude_types=exclude,
    magr_min=args.r[0],
    magr_max=args.r[1],
    dec_min=args.dec[0],
    dec_max=args.dec[1],
    brick_primary=not args.noprimary,
    overwrite=args.overwrite,
    workers=args.workers,
    tmp_folder=args.tmp,
    overwrite_tmp=args.otmp,
  )
  
def handle_cutout(args: Namespace):
  cols = []
  if args.ra is not None:
    cols.append(args.ra)
  if args.dec is not None:
    cols.append(args.dec)
  if not _is_numeric(args.pixscale) and args.pixscale != 'auto':
    cols.append(args.pixscale)
  
  df = read_table(args.cat, columns=cols or None)
  if args.limit is None:
    df = df.iloc[args.offset:]
  else:
    df = df.iloc[args.offset:args.limit]
  
  ra_col, dec_col = guess_coords_columns(df, args.ra, args.dec)
  ra = df[ra_col].values * u.deg
  dec = df[dec_col].values * u.deg
  shape_e1 = None
  shape_e2 = None
  shape_r = None
  mag_r = None
  if args.pixscale == 'auto':
    pixscale = 'auto'
    mag_r = df[args.magr].values
    if args.shape1 is not None and args.shape2 is not None:
      shape_e1 = df[args.shape1].values
      shape_e2 = df[args.shape2].values
    elif args.shaper is not None:
      shape_r = df[args.shaper].values
  elif _is_numeric(args.pixscale):
    pixscale = float(args.pixscale)
  else:
    pixscale = df[args.pixscale].values
  
  save_path = Path(args.output)
  if args.fnames is not None:
    save_path = [save_path / f'{f}.{args.format}' for f in df[args.fnames].values]
  
  batch_cutout(
    ra=ra,
    dec=dec,
    pixscale=pixscale,
    save_path=save_path,
    workers=args.workers,
    overwrite=args.overwrite,
    width=args.width,
    height=args.height,
    size=args.size,
    shape_e1=shape_e1,
    shape_e2=shape_e2,
    shape_r=shape_r,
    mag_r=mag_r,
    fmt=args.format,
    bands=args.bands,
    layer=args.layer,
    compress_fits=args.compress,
  )
  

def handle_axmatch(args: Namespace):
  from pylegs.archive import CrossMatcher
  cm = CrossMatcher.from_table(
    table=args.input, 
    radius=args.radius, 
    ra_col=args.ra, 
    dec_col=args.dec, 
    fmt=args.fmt,
    unit=args.unit,
  )
  cm.match(
    output_path=args.output,
    bricks_dir=args.cache,
    columns=args.columns,
    overwrite=args.overwrite,
    include_brickname=args.brickname,
    include_dr=args.dr,
  )
  
  
  
def handle_txmatch(args: Namespace):
  from pylegs.tap import ls_crossmatch
  
  df = read_table(args.input)
  ra_col, dec_col = guess_coords_columns(df, args.ra, args.dec)
  
  if args.rarange is not None:
    df = df[df[ra_col].between(*args.rarange)]
  
  if args.decrange is not None:
    df = df[df[dec_col].between(*args.decrange)]
  
  ls_crossmatch(
    table=df,
    columns=args.columns,
    radius=args.radius,
    save_path=args.output,
    ra_col=ra_col,
    dec_col=dec_col,
    overwrite=args.overwrite,
    cache_dir=args.cache,
    overwrite_cache=args.overwritecache,
    workers=args.workers,
  )



def entrypoint():
  parser = ArgumentParser(
    prog='pylegs', 
    description='Python client for accessing Legacy Survey data'
  )
  
  subparser = parser.add_subparsers(dest='subprog')
  dlcat = subparser.add_parser(
    'dlcat', help='Tool for download Legacy Survey catalog based on square area'
  )
  dlcat.add_argument(
    'output', action='store', type=str, help='Path of the output table'
  )
  dlcat.add_argument(
    '--ra', action='store', nargs=2, type=float, default=[0, 360], 
    help='Two values specifying the RA range in degrees. Default: 0 360'
  )
  dlcat.add_argument(
    '--delta', action='store', default='10 arcmin',
    help=('The value of the angle interval that the ra axis will be divided. '
          'The unit must be specified. E.g: 1.2 deg, 20 arcmin, 14 arcsec. '
          'Default: 10 arcmin')
  )
  dlcat.add_argument(
    '--dec', action='store', nargs=2, type=float, default=[-90, 90], 
    help='Two values specifying the DEC range in degrees. Default: -90 90'
  )
  dlcat.add_argument(
    '--cols', action='store', nargs='+', default=None,
    help=f'Column names to retrieve. Default: {" ".join(DEFAULT_CATALOG_COLUMNS)}'
  )
  dlcat.add_argument(
    '--table', action='store', default='ls_dr10.tractor',
    help='Fully qualified table name following the format: <schema_name>.<table_name>. Default: ls_dr10.tractor'
  )
  dlcat.add_argument(
    '--types', action='store', nargs='+', default=['REX', 'DEV', 'EXP', 'SER'],
    choices=['PSF', 'REX', 'DEV', 'EXP', 'SER'],
    help=('Morphological types to allow in final table.'
          'By default, only PSF type (stars) are removed. '
          'Possible values: PSF, REX, DEV, EXP, SER. Default: REX DEV EXP SER')
  )
  dlcat.add_argument(
    '--r', action='store', type=float, nargs=2, default=[10, 21],
    help='The magnitude range in band r. Default: 10 21'
  )
  dlcat.add_argument(
    '--noprimary', action='store_true', 
    help='Include no primary objects. By default, only primary objects are included.'
  )
  dlcat.add_argument(
    '--overwrite', action='store_true', 
    help='Use this flag to overwrite the destinaton path if the file exists'
  )
  dlcat.add_argument(
    '--workers', action='store', type=int, default=7,
    help='Number of parallel queries that will be sent to server. Default: 7'
  )
  dlcat.add_argument(
    '--tmp', action='store', default=None,
    help='Temp folder to store partial tables. Default: none'
  )
  dlcat.add_argument(
    '--otmp', action='store_true',
    help='Set this flag to overwrite partial tables in temp folder, if exists'
  )
  
  
  
  cutout = subparser.add_parser('cutout', help='Legacy stamps cutout')
  cutout.add_argument(
    'output', action='store',
    help='The folder path to save the figures'
  )
  cutout.add_argument(
    '--cat', '-c', action='store', default=None,
    help='The path of the catalog to be downloaded. Default: None'
  )
  cutout.add_argument(
    '--ra', action='store', default=None,
    help='The name of the RA column. Default: auto, the package will try to infer',
  )
  cutout.add_argument(
    '--dec', action='store', default=None,
    help='The name of the DEC column. Default: auto, the package will try to infer',
  )
  cutout.add_argument(
    '--fnames', '-f', action='store', default=None,
    help=(
      'The name of the column to be used as filename for each stamp.'
      'If not specified, this package will compute the IAUNAME for each '
      'object based on position RA and DEC and will use the IAUNAME as filename. '
      'Default: None'
    )
  )
  cutout.add_argument(
    '--pixscale', '-p', action='store', default=0.4,
    help=(
      'A float indicating a static pixscale for all stamps in arcsec/pixel, '
      'a string with the name of the pixscale column in the catalog, '
      'or "auto" to compute pixscale automatically. For the last option, '
      'mag_r, shape_e1 and shape_e2 must be set to compute pixscale using '
      'elliptical fit or mag_r and shape_r to use radial fit. Default: 0.4'
    ),
  )
  cutout.add_argument(
    '--limit', '-l', action='store', type=int, default=None,
    help=(
     'The row limit to download, starting with 0. '
     'Default: None (download the full catalog)'
    )
  )
  cutout.add_argument(
    '--offset', '-o', action='store', type=int, default=0,
    help=(
      'The index of the row to start the download, starting with 0. '
      'Default: 0 (the first row)'
    )
  )
  cutout.add_argument(
    '--format', action='store', default='jpg', choices=['jpg', 'fits'],
    help='The image format. Default: jpg'
  )
  cutout.add_argument(
    '--bands', action='store', default=None,
    help=(
      'A string representating the bands (griz) to dowload. '
      'Default: None (all available bands - griz)'
    )
  )
  cutout.add_argument(
    '--layer', action='store', default=None,
    help='The image layer. More details in Legacy documentation. Default: ls10-griz'
  )
  cutout.add_argument(
    '--width', action='store', type=int, default=256,
    help=(
      'The width of the image in pixels. Default: 256'
    )
  )
  cutout.add_argument(
    '--height', action='store', type=int, default=256,
    help=(
      'The height of the image in pixels. Default: 256'
    )
  )
  cutout.add_argument(
    '--size', '-s', action='store', type=int, default=None,
    help=(
      'The size of the image in pixels (square image). The arguments --width '
      'and --height are ignored if this argument is specified. Default: 256'
    )
  )
  cutout.add_argument(
    '--shape1', action='store', default=None,
    help='Name of the shape_e1 column'
  )
  cutout.add_argument(
    '--shape2', action='store', default=None,
    help='Name of the shape_e2 column'
  )
  cutout.add_argument(
    '--shaper', action='store', default=None,
    help='Name of the shape_r column'
  )
  cutout.add_argument(
    '--magr', action='store', default=None,
    help='Name of the mag_r column'
  )
  cutout.add_argument(
    '--compress', action='store_true',
    help='Compress fits stamp'
  )
  cutout.add_argument(
    '--overwrite', action='store_true', 
    help='Overwrite stamps'
  )
  cutout.add_argument(
    '--workers', action='store', type=int, default=6,
    help=(
      'The number of workers to spawn, meaning the number of parallel downloads. '
      'Default: 6'
    )
  )
  
  
  axmatch = subparser.add_parser('axmatch', help='Crossmatch Archive Server')
  axmatch.add_argument(
    'input', action='store', 
    help='Input table to crossmatch against Legacy Archive Server'
  )
  axmatch.add_argument(
    'output', action='store',
    help='Output table path'
  )
  axmatch.add_argument(
    '--radius', action='store', default='1 arcsec',
    help=(
      'Crossmatch radius, the unit must be specified. e.g. --radius 1.5 arcsec.'
      ' Default: 1 arcsec'
    )
  )
  axmatch.add_argument(
    '--cache', action='store', default='legacy_bricks',
    help=(
      'The cache dir. This folder will store the partial tables.' 
      ' Default: "legacy_bricks"'
    )
  )
  axmatch.add_argument(
    '--columns', action='store', nargs='+',
    help=(
      f'The columns to get from service. Default: {" ".join(DEFAULT_CATALOG_COLUMNS)}'
    )
  )
  axmatch.add_argument(
    '--ra', action='store', default=None,
    help='The name of the RA column. Default: auto, the package will try to infer',
  )
  axmatch.add_argument(
    '--dec', action='store', default=None,
    help='The name of the DEC column. Default: auto, the package will try to infer',
  )
  axmatch.add_argument(
    '--ifmt', action='store', default=None,
    help=(
      'Input table format, e.g. csv, parquet, fits. Default: auto, the package '
      'will try to infer from filename'
    )
  )
  axmatch.add_argument(
    '--unit', action='store', default='deg',
    help=(
      'Unit of the coordinates columns (RA and DEC) in inpu table. '
      'Default: deg'
    )
  )
  axmatch.add_argument(
    '--overwrite', action='store_true',
    help='Overwrites the output table'
  )
  axmatch.add_argument(
    '--brickname', action='store_true',
    help='Add brick name column in output table'
  )
  axmatch.add_argument(
    '--dr', action='store_true',
    help='Add data release column in output table'
  )
  
  
  
  txmatch = subparser.add_parser('txmatch', help='Crossmatch TAP Server')
  txmatch.add_argument(
    'input', action='store', 
    help='Input table to crossmatch against Legacy TAP Server'
  )
  txmatch.add_argument(
    'output', action='store',
    help='Output table path'
  )
  txmatch.add_argument(
    '--radius', action='store', default='1 arcsec',
    help=(
      'Crossmatch radius, the unit must be specified. e.g. --radius 1.5 arcsec.'
      ' Default: 1 arcsec'
    )
  )
  txmatch.add_argument(
    '--columns', action='store', nargs='+',
    help=(
      f'The columns to get from service. Default: {" ".join(DEFAULT_CATALOG_COLUMNS)}'
    )
  )
  txmatch.add_argument(
    '--ra', action='store', default=None,
    help='The name of the RA column. Default: auto, the package will try to infer',
  )
  txmatch.add_argument(
    '--dec', action='store', default=None,
    help='The name of the DEC column. Default: auto, the package will try to infer',
  )
  txmatch.add_argument(
    '--rarange', action='store', type=float, nargs=2, default=None,
    help=(
      'Filter the input table RA by a specified range in degrees. '
      'E.g. --rarange 180 210. Default: None - no filter'
    )
  )
  txmatch.add_argument(
    '--decrange', action='store', type=float, nargs=2, default=None,
    help=(
      'Filter the input table DEC by a specified range in degrees. '
      'E.g. --decrange 10 90. Default: None - no filter'
    )
  )
  txmatch.add_argument(
    '--cache', action='store', default=None,
    help=(
      'Cache dir - folder to store partial tables. Default: None - the folder '
      'will be created in temp dir'
    )
  )
  txmatch.add_argument(
    '--overwritecache', action='store_true',
    help=(
      'Set this flag to overwrite partial tables in cache dir.'
    )
  )
  txmatch.add_argument(
    '--overwrite', action='store_true',
    help='Overwrites the output table'
  )
  txmatch.add_argument(
    '--workers', action='store', type=int, default=8,
    help='Number of parallel queries that will be sent to server. Default: 8'
  )
  
  
  
  handler_map = {
    'dlcat': handle_dlcat,
    'cutout': handle_cutout,
    'axmatch': handle_axmatch,
    'txmatch': handle_txmatch,
  }
  args = parser.parse_args()
  handler = handler_map.get(args.subprog)
  if handler:
    handler(args)
  else:
    parser.print_help()
  


if __name__ == '__main__':
  entrypoint()