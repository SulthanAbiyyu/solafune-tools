import os

import solafune_tools

data_dir = solafune_tools.settings.get_data_directory()


def create_basemap(
    start_date="2023-05-01",
    end_date="2023-08-01",
    aoi_geometry_file=os.path.join("tests", "data-test", "geojson", "sample.geojson"),
    bands=["B02", "B03", "B04"],
    mosaic_epsg="Auto",
    mosaic_resolution=100,
) -> os.PathLike:
    """
    Creates a basemap given a geometry file, date range, bands and output resolution
    """
    plc_stac_catalog = solafune_tools.image_fetcher.planetary_computer_stac_query(
        start_date=start_date, end_date=end_date, aoi_geometry_file=aoi_geometry_file
    )

    tiffile_dir = solafune_tools.image_fetcher.planetary_computer_fetch_images(
        dataframe_path=plc_stac_catalog,
        bands=bands,
        outfile_dir="Auto",
    )

    local_stac_catalog = solafune_tools.make_catalog.create_local_catalog_from_existing(
        input_catalog_parquet=plc_stac_catalog,
        bands=bands,
        tif_files_dir=tiffile_dir,
        outfile_dir="Auto",
    )

    mosaic_file_loc = solafune_tools.make_mosaic.create_mosaic(
        local_stac_catalog=local_stac_catalog,
        aoi_geometry_file=aoi_geometry_file,
        outfile_loc="Auto",
        out_epsg=mosaic_epsg,
        resolution=mosaic_resolution,
    )

    mosaics_catalog = solafune_tools.make_catalog.create_local_catalog_from_scratch(
        infile_dir=os.path.dirname(mosaic_file_loc), outfile_loc="Auto"
    )

    return mosaics_catalog
